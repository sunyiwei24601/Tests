
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
from poseidon.components.textAnalysis.stringIndexerCom_bak import StringIndexerCom

# hdfs client
client = CommonUtil.insecureHdfsClient('default', 'glzheng')


class RandomForestComCopy():

    # This method is used to initialize the classfier, one thing to note is the labelCol is set to indexed which is not
    # default value 'label',cause we process the original data by StringIndexer which generate the new col named indexed
    # from label of original
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
    def randomForestTrainer1(jobj, input_data):

        try:
            # spark initializer
            (conf, spark, sc) = SparkUtil.getSpark()
            # get param
            algopt = jobj.get('algopt', "")     # algorithm args
            commonopt = jobj.get('commonopt', "")   # common args
            # rf classifier
            rf = RandomForestComCopy.getRandomForestClassifier(algopt)
            # get feature value
            featuresCol = algopt.get('featuresCol', "")
            input_data = commonopt.get('input', "")
            output_data = commonopt.get('output', "")
            print(input_data)
            if not input_data:
                return 1000
            elif type(input_data) == type('str'):
                print(111)
                # the input data is a hive table,at this time we need to transform hive table into a data frame

                # 1. read features from hive table
                sql = "select %s from %s" % (featuresCol, input_data)
                cursor = CommonUtil.initHiveCursor('default', '', '')
                clist = CommonUtil.getHiveSqlResult(cursor, sql)
                print(clist)
                hlist = []
                if featuresCol.find(',') != -1:
                    # features contains mutiple columns
                    for items in clist:
                        tup = (list(items))
                        hlist.append(tup)
                # ???
                df = spark.createDataFrame(hlist, ['features'])

                model = rf.fit(df)

                # store randomforest
                basepath = '/tmp/'
                rfc_path = basepath + 'poseidon/jlye_rf/result'
                # if this path existed,del it
                CommonUtil.delIfExistsInHdfs(client, rfc_path)
                model.save(rfc_path)
                return model

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0




