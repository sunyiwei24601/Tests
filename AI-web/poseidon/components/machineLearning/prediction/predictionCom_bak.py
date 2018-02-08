# -*- coding:UTF-8 -*-
from __future__ import print_function
import json
from flask import jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorIndexer

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

# hdfs client
client = CommonUtil.insecureHdfsClient('http://dasrv03.novalocal:50070/', 'glzheng')


class PredictionCom():
    """
    This method is actually a transformer in spark,a spark transformer accept 2 args, one is model and the other one is the data
    is going to be transformed or predicted. One thing to note is the df is a dataframe if the input of the commonopt of the jobj is
    not a hive table, if the input is the hive table, we need to convert the hive table to dataframe.
    If the features of the algopt contains only 1 column, then it is probably the hive table applied to the word2vec model to transformer.
    If the features of the algopt contains more than 2 columns, then we gonna assemble these columns together as a features column and
    convert it to the dataframe.
    """

    """
    jobj: user configuration param
    model: in1
    data: in2(dataframe/hive table)
    """
    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   note:model
        in2:xxx   note:input data which is of df type
    outs is a array contains:
        out1      note:predicted data which is of df type
    '''

    @staticmethod
    # def predictionTransformer(jobj, model, data):
    def predictionComProcesser(tid, jobj, model, data):

        try:
            (conf, spark, sc) = SparkUtil.getSpark()
            algopt = jobj.get('algopt', "")  # algorithm args
            commonopt = jobj.get('commonopt', "")  # common args
            if algopt:
                featuresCol = algopt.get('featuresCol', "features")
                predictionCol = algopt.get('predictionCol', "prediction")
                probabilityCol = algopt.get('probabilityCol', "probability")
                if not data:
                    return 1000

                elif type(data) == type('str'):
                    # the input data is a hive table,at this time we need to transform hive table into a data frame
                    # 1. read features from hive table
                    sql = "select %s from %s" % (featuresCol, data)
                    cursor = CommonUtil.initHiveCursor('default', '', '')  # hive连接初始化

                    clist = CommonUtil.getHiveSqlResult(cursor, sql)
                    hlist = []
                    # 2. if the features contains one column, split each line
                    if featuresCol.find(',') != -1:
                        # features contains mutiple columns
                        for items in clist:
                            tup = (Vectors.dense(list(items)),)
                            hlist.append(tup)
                    else:
                        # features contains only one column
                        for line in clist:
                            tup = (Vectors.dense(re.split(u"\u0020", line[0].decode('utf-8'))))
                            hlist.append(tup)
                    data = spark.createDataFrame(hlist, ["features"])
                # test
                if not model:
                    modelPath = "/tmp/jlye/rf_model"
                    model = RandomForestClassificationModel.load(modelPath)
                # make a prediction i.e. make a transformation
                predictions = model.transform(data)
                # if predictions
                predictions = predictions.withColumnRenamed(predictionCol, "pred")
                predictions = predictions.withColumnRenamed(probabilityCol, "prol")
                # test
                predictions.printSchema()
                predictions.show()
                return predictions

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 'error!'





