from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType, StructField
from pyspark import SparkContext


class Predictor:
    price_model = None
    discount_model = None
    spark = None
    spark_context = SparkContext(
        master='local',
        appName='DecisionTreeRegression',
        sparkHome='/home/ground/bigdata/spark',
    )

    def __init__(self, model_name):
        self.spark = SparkSession(self.spark_context)
        if model_name == 'bjs_kmg':
            self.price_model = PipelineModel.load('hdfs://localhost:9000/spark/bjs_kmg_price_dt.model')
            self.discount_model = PipelineModel.load('hdfs://localhost:9000/spark/bjs_kmg_discount_dt.model')

    def predict(self, features):
        schema = StructType([
            StructField('airline', StringType(), False),
            StructField('dmonth', IntegerType(), False),
            StructField('dday', IntegerType(), False),
            StructField('dweek', IntegerType(), False),
            StructField('dhour', IntegerType(), False),
            StructField('ahour', IntegerType(), False),
            StructField('ahead', IntegerType(), False),
        ])
        data = self.spark.createDataFrame(features, schema)
        return self.price_model.transform(data).select('prediction')


if __name__ == '__main__':
    p = Predictor('bjs_kmg')
    p.predict({'airline': '3U', 'dmonth': 5, 'dday': 18, 'dweek': 7, 'dhour': 22, 'ahour': 1, 'ahead': 45})
