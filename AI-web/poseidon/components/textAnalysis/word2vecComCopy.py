# -*- coding: utf-8 -*-
"""
If the input data is hive table,then the format is:
    [('我是 中国 人','正'),
     ('机器 学习 太 棒','正'),
    ]
NOTE:the first field has been tokenized by tokenizer,
"""
from __future__ import print_function
import json
from flask import jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import Word2Vec

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

#hdfs client
client = CommonUtil.insecureHdfsClient('http://192.168.11.176:50070/', 'glzheng')


class Word2vecComponent():
    @staticmethod
    def getWord2vec(opt):
        return Word2Vec(vectorSize=opt.get('vectorSize', 100),
                        minCount=opt.get('minCount', 5),
                        numPartitions=opt.get('numPartitions', 1),
                        stepSize=opt.get('stepSize', 0.025),
                        maxIter=opt.get('maxIter', 1),
                        seed=opt.get('seed', None),
                        inputCol='sentence',
                        outputCol=opt.get('outputCol', 'vectors'),
                        windowSize=opt.get('windowSize', 5),
                        maxSentenceLength=opt.get('maxSentenceLength', 1000))

    @staticmethod
    def word2vecTrainered(jobj):

        try:
            (conf, spark, sc) = SparkUtil.getSpark()
            algopt = jobj.get('algopt', "") # algorithm args
            commonopt = jobj.get('commonopt', "") # common args

            inputCol = None
            if algopt:
                # get the input column user specified to train the word2vec
                inputCol = algopt.get('inputCol', None)

            if not commonopt:
                # commonopt arg can not be null
                return 1005
            else:
                # input of this component
                input_data = commonopt.get('input', "")
                if not input_data:
                    # commonopt.input_data arg can not be null
                    return 1000
                # see if the type of the input data:hive table or dataframe
                # if type(input_data) == type('str'.decode('utf-8')):
                    # hive table,then we gonna read hive table to dataframe which can be used by the algorithm in spark
                if input_data != 'df':
                    # 1. read hive table to list
                    cursor = CommonUtil.initHiveCursor('default', '', '')
                    sql = 'select %s from %s' % (inputCol, input_data)
                    contents = CommonUtil.getHiveSqlResult(cursor, sql)
                    training_voc = []
                    for content in contents:
                        tup = (re.split(u"\u0020", content[0].decode('utf-8')),)
                        training_voc.append(tup)
                    df = spark.createDataFrame(training_voc, ["sentence"])
                    word2Vec = Word2vecComponent.getWord2vec(algopt)
                    model = word2Vec.fit(df)
                    # # store the word2vec
                    # basepath = '/tmp/'
                    # word2vecPath = basepath+'poseidon_jlye/result'
                    # # if this path existed,del it
                    # CommonUtil.delIfExistsInHdfs(client, word2vecPath)
                    #
                    # model.save(word2vecPath)
                    model.getVectors().show()
                    return model
                else:
                    # dataframe,then we can feed this data to the algorithm directly
                    #  without processing it which is conveniently
                    # or other data types, leave it alone for now
                    return 0

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0




