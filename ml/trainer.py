from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils

if __name__ == "__main__":
    sc = SparkContext(
        master='spark://hadoop-1:7077',
        appName='DecisionTreeRegressionTest',
        sparkHome='/home/ground/bigdata/spark',
    )

    data = MLUtils.loadLibSVMFile(sc, '/user/ground/sample_libsvm_data.txt')
    trainingData, testData = data.randomSplit([0.7, 0.3])

    """
    参数：
        data：pyspark.rdd of LabeledPoint, 标签是实数
        categoricalFeaturesInfodict: Map storing arity of categorical features.
            An entry (n -> k) indicates that feature n is categorical with k categories indexed from 0: {0, 1, …, k-1}.
        maxDepth: 树深度，默认5
        maxBins: Number of bins used for finding splits at each node. (default: 32)
        minInstancesPerNodeint: Minimum number of instances required at child nodes to create the parent split. (default: 1)
        minInfoGainfloat: Minimum info gain required to create a split. (default: 0.0)
    """
    model = DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={}, maxDepth=5,
                                        maxBins=32)

    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    testMSE = labelsAndPredictions.map(lambda lp: (lp[0] - lp[1]) * (lp[0] - lp[1])).sum() / float(testData.count())
    print('Test Mean Squared Error = ' + str(testMSE))
    print('Learned regression tree model:')
    print(model.toDebugString())

    # Save and load model
    model.save(sc, "target/myDecisionTreeRegressionModel")
    sameModel = DecisionTreeModel.load(sc, "target/myDecisionTreeRegressionModel")
