from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType, StructField
from pyspark import SparkContext
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, timedelta


def get_db():
    """
    获取数据库连接
    """
    db = psycopg2.connect(
        dbname='ground',
        user='ground',
        password='ground',
        host='localhost',
        port=5432,
        cursor_factory=RealDictCursor
    )

    return db


def predict_bjs_kmg(sc):
    spark = SparkSession(sc)
    model = PipelineModel.load('hdfs://localhost:9000/spark/bjs_kmg_price_dt.model')
    schema = StructType([
        StructField('tid', IntegerType(), False),
        StructField('airline', StringType(), False),
        StructField('dmonth', IntegerType(), False),
        StructField('dday', IntegerType(), False),
        StructField('dweek', IntegerType(), False),
        StructField('dhour', IntegerType(), False),
        StructField('ahour', IntegerType(), False),
        StructField('ahead', IntegerType(), False),
    ])

    db = get_db()
    with db.cursor() as cur:
        cur.execute('''select *
                       from ground.ticket 
                       where dcity_code=%s and acity_code=%s and cdate=%s''',
                    ('BJS', 'KMG', date.today()))
        result = cur.fetchall()

    keys = ['tid', 'airline', 'dmonth', 'dday', 'dweek', 'dhour', 'ahour', 'ahead']
    features = []
    for r in result:
        features += [dict(zip(keys, [r['id'],
                                     r['airline_code'],
                                     int(r['ddate'].month),
                                     int(r['ddate'].day),
                                     r['ddate'].isoweekday(),
                                     int(r['dtime'].hour),
                                     int(r['atime'].hour),
                                     i]))
                     for i in range(48)]

    data = spark.createDataFrame(features, schema)
    predictions = model.transform(data).collect()

    with db.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS ground.bjs_kmg_price')
        cur.execute(
            '''CREATE TABLE ground.bjs_kmg_price
               (
                    id         serial PRIMARY KEY NOT NULL,
                    ticket_id  int4,
                    price      float4,
                    cdate      date
                )'''
        )
    db.commit()

    with db.cursor() as cur:
        for row in predictions:
            cur.execute(
                'INSERT INTO ground.bjs_kmg_price (ticket_id, price, cdate) VALUES (%s, %s, %s)',
                (row['tid'], row['prediction'], date(2021, row['dmonth'], row['dday']) - timedelta(row['ahead']))
            )

    db.commit()
    db.close()


if __name__ == '__main__':
    sc = SparkContext(
        master='spark://localhost:7077',
        appName='DecisionTreeRegression',
        sparkHome='/home/ground/bigdata/spark',
    )

    predict_bjs_kmg(sc)
