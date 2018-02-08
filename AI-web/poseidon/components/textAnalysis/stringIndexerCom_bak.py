# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from flask import jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

# hdfs client
client = CommonUtil.insecureHdfsClient('http://dasrv03.novalocal:50070/', 'glzheng')


class StringIndexerCom():
    def __init__(self):
        pass
    @staticmethod
    def getStringIndexer(opt):
        return StringIndexer(inputCol=opt.get('inputCol', None),
                             outputCol=opt.get('outputCol', None),
                             handleInvalid="error")

    @staticmethod
    def stringIndexerTrainer(jobj, df):

        try:
            (conf, spark, sc) = SparkUtil.getSpark()
            algopt = jobj.get('algopt', "")  # algorithm args
            commonopt = jobj.get('commonopt', "")  # common args

            inputCol = None
            if algopt:
                # get the input column user specified to train the word2vec
                inputCol = algopt.get('inputCol', None)
                outputCol = algopt.get('outputCol', None)
                if not inputCol:
                    return 1007
                if not outputCol:
                    return 1008
            else:
                return 1006

            if not commonopt:
                # commonopt arg can not be null
                return 1005
            else:
                # input of this component
                input_data = commonopt.get('input', "")
                output_data = commonopt.get('output', "")
                if not input_data:
                    # commonopt.input_data arg can not be null
                    return 1000
                # see if the type of the input data:hive table or dataframe
                if type(input_data) == type('str'.decode('utf-8')):
                    # hive table,then we gonna read hive table to dataframe which can be used by the algorithm in spark

                    # 1. read hive table to list
                    cursor = CommonUtil.initHiveCursor('default','','')
                    sql = 'select %s from %s' % (inputCol, input_data)
                    lines = CommonUtil.getHiveSqlResult(cursor, sql)
                    hlist = []
                    # only one column
                    for line in lines:
                        tup = (line[0].decode('utf-8'),)
                        hlist.append(tup)
                    doc = spark.createDataFrame(hlist, [inputCol])
                    stringIndexer = StringIndexerCom.getStringIndexer(algopt)
                    model = stringIndexer.fit(doc)
                    # store the word2vec
                    basepath = '/tmp/'
                    word2vecPath = basepath+'poseidon/stringIndexerModel/result'
                    # if this path existed,del it
                    CommonUtil.delIfExistsInHdfs(client, word2vecPath)
                    model.save(word2vecPath)

                    # transform training data with model
                    indexed_doc = model.transform(doc)

                    # write csv and load csv into a new hive table
                    sql = 'select * from %s' % input_data
                    newlines = CommonUtil.getHiveSqlResult(cursor, sql)

                    # csv_content = list(newlines)
                    csv_content = []
                    if output_data:
                        indexed_doc_list = indexed_doc.collect()
                        # zip the indexed_doc transformed by model into the csv_content
                        for i in range(len(newlines)):
                            newCol = indexed_doc_list[i][outputCol]
                            newlist = list(newlines[i])
                            newlist.append(str(newCol))
                            csv_content.append(newlist)

                        # create output hive table by input hive table and outputCol specified by user
                        # get desc of hive table
                        desc = CommonUtil.getDescByHiveTable(cursor, input_data)
                        desc += ",%s double" % outputCol
                        # create new table by the desc of last step
                        CommonUtil.createHiveTableWithSerDe(cursor, output_data, desc, 'csv')

                        # load csv file into hive table
                        filename = '%s.csv' % CommonUtil.generateRandomStr()
                        CommonUtil.writeList2CSV(client, csv_content, '/tmp/%s' % filename)
                        CommonUtil.loadFile2HiveSerDeTable(cursor, '/tmp/%s' % filename, output_data)
                        return 1
                else:
                    # dataframe
                    return 0
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0




