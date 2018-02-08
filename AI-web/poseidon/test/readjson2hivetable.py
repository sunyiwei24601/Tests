
"""
read json file to hive table

"""
from poseidon.util.commonUtil import CommonUtil
from json import dump,load
import json
import os


def insertJsonFile2HiveTable(cursor,inpath,tablename):
    CommonUtil.loadFile2HiveSerDeTable(cursor,inpath,tablename)

if __name__ == '__main__':
    cursor = CommonUtil.initHiveCursor('default','','')
    train_table = 'default.emotion_train'
    test_table = 'default.emotion_test'
    # inpath = '/storeage/glzheng/qingbaodata/commentEmotionJSON2.json'
    train_path = '/glzheng/sentimental_analysis/qingbaodata/commentEmotionJSON_train.json'
    test_path = '/glzheng/sentimental_analysis/qingbaodata/commentEmotionJSON_test.json'
    #create tables
    # CommonUtil.createHiveTableWithSerDe(cursor,train_table,'commentText string,commentEmotions string')
    # CommonUtil.createHiveTableWithSerDe(cursor,test_table,'commentText string,commentEmotions string')



    # insertJsonFile2HiveTable(cursor,train_path,train_table)
    # insertJsonFile2HiveTable(cursor,test_path,test_table)

    CommonUtil.createHiveTableWithSerDe(cursor,'default.testjson','commentText string,commentEmotions string')
    insertJsonFile2HiveTable(cursor, '/glzheng/sentimental_analysis/qingbaodata/commentEmotionJSON2.json','default.testjson')