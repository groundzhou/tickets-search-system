from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import RFormula
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.sql import HiveContext


def train1(spark_config):
    """
    todo: 调整参数
    """
    # 1. 从Hive导入数据
    sql_context = HiveContext(spark_config)
    data = sql_context.sql('select * from flight.bjs_kmg_2')

    # 2. 查看数据类型，预览数据
    # df.printSchema()
    # df.show(3)

    # 3. 插补删除缺失值
    data.na.drop('any')

    # 4. 分析数值特征
    # 5. 分析分类特征
    # 6. 将分类变量转换为标签
    # airlineIndexer = StringIndexer(inputCol='airline', outputCol='indexedAirline').fit(df)
    # df1 = airlineIndexer.transform(df)
    # df1.show(3)

    # 7. 特征化并构建模型 R模型公式
    formula = RFormula(formula='discount ~ airline + dmonth + dday + dweek + dhour + ahour + ahead').fit(data)

    # 8. 建立机器学习模型并训练
    (training_data, test_data) = data.randomSplit([0.7, 0.3])
    dt = DecisionTreeRegressor(maxDepth=20, maxBins=32, maxMemoryInMB=2048)
    pipeline = Pipeline(stages=[formula, dt])

    # 训练模型
    model = pipeline.fit(training_data)

    # 预测
    predictions = model.transform(test_data)
    predictions.select("prediction", "label", "features").show(5)

    # 计算RMSE，验证效果
    evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)
    print(model.stages[1])


def train2(spark_config):
    """
    todo: 预测最低价
    """
    pass


if __name__ == "__main__":
    sc = SparkContext(
        master='spark://hadoop-1:7077',
        appName='DecisionTreeRegressionTest',
        sparkHome='/home/ground/bigdata/spark',
    )

    train1(sc)
    sc.stop()
