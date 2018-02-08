
from __future__ import print_function
import json
from flask import  jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import RandomForestClassifier

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

#hdfs client
client = CommonUtil.insecureHdfsClient('http://dasrv03.novalocal:50070/','glzheng')


class RandomForestService():

    #This method is used to initialize the classfier, one thing to note is the labelCol is set to indexed which is not
    #default value 'label',cause we process the original data by StringIndexer which generate the new col named indexed
    #from label of original
    @staticmethod
    def getRandomForestClassifier(opt):
        rf = RandomForestClassifier(featuresCol="features",
                                    labelCol="indexed",
                                    predictionCol=opt.get('predictionCol', "prediction"),
                                    probabilityCol=opt.get('probabilityCol', "probability"),
                                    rawPredictionCol=opt.get('rawPredictionCol', "rawPrediction"),
                                    maxDepth=opt.get('maxDepth', 5),
                                    maxBins=opt.get('maxBins', 32),
                                    minInstancesPerNode=opt.get('minInstancesPerNode', 1),
                                    minInfoGain=opt.get('minInfoGain', 0.0),
                                    maxMemoryInMB=opt.get('maxMemoryInMB', 256),
                                    cacheNodeIds=opt.get('cacheNodeIds', False),
                                    checkpointInterval=opt.get('checkpointInterval', 10),
                                    impurity=opt.get('impurity', "gini"),
                                    numTrees=opt.get('numTrees', 20),
                                    featureSubsetStrategy=opt.get('featureSubsetStrategy', "auto"),
                                    seed=opt.get('seed', None))
        return rf

    @staticmethod
    def randomForestProcesser(jobj):

        try:
            (conf,spark,sc) = SparkUtil.getSpark()

            algopt = jobj.get('algopt', "") # algorithm args
            commonopt = jobj.get('commonopt', "") # common args
            train_path = commonopt.get('train_path', "/glzheng/spark_example_data/sample_libsvm_data_train.txt")
            test_path = commonopt.get('test_path', "")
            respath = commonopt.get('respath', "/glzheng/tmp/randomForest_result")

            rf = RandomForestService.getRandomForestClassifier(algopt)
            # rf = RandomForestClassifier(numTrees=3, maxDepth=5, labelCol="indexed", seed=42, featuresCol="model") #accuracy: 0.73304825901

            training_data = SparkUtil.loadData(spark,sc,'libsvm',train_path,algopt)

            test_data = None
            if not test_path:
                print('####testdata will be split out from training data')
                (training_data, test_data) = training_data.randomSplit([0.8, 0.2])
            else:
                test_data = SparkUtil.loadData(spark,sc,'libsvm',test_path,algopt)

            randomForest_model = rf.fit(training_data)

            # Make predictions.
            predictions = randomForest_model.transform(test_data)

            # Select example rows to display.
            # predictions.select("prediction", "indexed", "model").show(5)

            result = SparkUtil.muti_eva_predictions('randomForestModel', predictions)

            CommonUtil.delIfExistsInHdfs(client,respath)
            rf.save(respath+'/estimator')#save the estimator
            randomForest_model.save(respath+'/model') # save the model

            # save the result i.e. the evaluation result
            with client.write(respath+'/evaluations.txt') as writer:
                writer.write(u'randomForestAccuracy: %s\n' % str(result))
            return 1
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0




