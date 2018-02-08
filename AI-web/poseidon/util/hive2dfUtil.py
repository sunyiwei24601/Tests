# -*- coding: utf-8 -*-
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil
from pyspark.ml.linalg import Vectors
import re


def getListBySql(sql):
    cursor = CommonUtil.initHiveCursor('default', '', '')
    return CommonUtil.getHiveSqlResult(cursor, sql)


class HiveToDF():

    def __init__(self):
        pass

    """
    jobj: 用户指定的参数-->对应hive表中的字段组成的数组[]
    input_data: default数据库中对用的hive_table
    """


    @staticmethod
    def hiveTB2df(jobj, input_data):
        try:
            # spark initializer
            (conf, spark, sc) = SparkUtil.getSpark()
            algopt = jobj.get('algopt', "")  # algorithm args
            # commonopt: [
            # col1: [],
            #    col2: [],
            #    ....
            #    coln: []
            # ]
            commonopt = jobj.get('commonopt', "")  # common args
            print(commonopt)

            # userDF：用户配置参数组合成的DataFrame形式
            multlist = []
            onlist = []
            hlist = []
            keys = []  # ['features','label']
            skList = []
            mkList = []
            if commonopt:
                for column in commonopt:
                    key = column  # features
                    keys.append(key)
                print(len(keys))
                # 2. if the value contains mutiple columns, split each line
                if len(keys) != 1:
                    for column in commonopt:
                        value = commonopt[column]
                        if value.find(',') != -1:
                            sql = "select {} from {}".format(value, input_data)
                            mlist = getListBySql(sql)
                            for items in mlist:
                                tuple = (Vectors.dense(list(items)))
                                multlist.append(tuple)
                            print(multlist)
                        else:
                            # value contains only one column
                            print(value)
                            sql = "select {} from {}".format(value, input_data)
                            olist = getListBySql(sql)
                            for line in olist:
                                tuple = line[0]
                                onlist.append(tuple)
                            print(onlist)
                    for col in zip(onlist, multlist):
                        hlist.append(col)
                    df = spark.createDataFrame(hlist, keys)
                    df.show()
                    return df

                else:
                    for column in commonopt:
                        value = commonopt[column]
                        if value.find(',') != -1:
                            sql = "select {} from {}".format(value, input_data)
                            print(sql)
                            klist = getListBySql(sql)
                            for item in klist:
                                tuple = (Vectors.dense(list(item)))
                                mkList.append(tuple)
                            df = spark.createDataFrame(mkList, keys)
                            return df
                        else:
                            # value contains only one column
                            sql = "select {} from {}".format(value, input_data)
                            cursor = CommonUtil.initHiveCursor('default', '', '')
                            olist = CommonUtil.getHiveSqlResult(cursor, sql)
                            print(type(olist))
                            for line in olist:
                                tuple = (re.split(u"\u0020", line[0].decode('utf-8')),)
                                skList.append(tuple)
                            print(type(skList))
                            df = spark.createDataFrame(skList, keys)
                            return df

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 'error!'



