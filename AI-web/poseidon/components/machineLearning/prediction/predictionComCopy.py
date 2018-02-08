# -*- coding:UTF-8 -*-
from __future__ import print_function
import json
from flask import jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors

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
    @staticmethod
    def predictionComProcesser(jobj, model, data):

        try:
            (conf, spark, sc) = SparkUtil.getSpark()

            algopt = jobj.get('algopt', "")  # algorithm args
            commonopt = jobj.get('commonopt', "")  # common args
            if not algopt:
                return 1006
            if not commonopt:
                return 1005
            features = algopt.get('features', "")
            predictionCol = algopt.get('predictionCol', "")
            probabilityCol = algopt.get('probabilityCol', "")
            if not features:
                return 1009

            input_data = commonopt.get('input', "")
            output_data = commonopt.get('output', "")
            if not input_data:
                return 1000
            elif input_data != 'df':
                # the input data is a hive table,at this time we need to transform hive table into a data frame

                # 1. read features from hive table
                sql = "select %s from %s" % (features, input_data)
                # 2. if the features contains one column, split each line
                cursor = CommonUtil.initHiveCursor('default', '', '')  # hive连接初始化
                clist = CommonUtil.getHiveSqlResult(cursor, sql)
                hlist = []
                if features.find(',') != -1:
                    # features contains mutiple columns
                    for items in clist:
                        tup = (list(items))
                        hlist.append(tup)
                else:
                    # features contains only one column
                    for line in clist:
                        tup = (re.split(u"\u0020", line[0].decode('utf-8')))
                        hlist.append(tup)
                df = spark.createDataFrame(hlist, [features])
            # make a prediction i.e. make a transformation
            predictions = model.transform(df)

            # if the output is a hive table, then we need to write this predictions into
            # a hive table. Or we return the predictions directly.
            if output_data != 'df':
                sql = 'insert into fin_result values(%s)' % predictions
                CommonUtil.getHiveSqlResult(cursor, sql)
            else:
                return predictions
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 'error!'




