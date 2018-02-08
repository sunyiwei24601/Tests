# -*- coding: utf-8 -*-
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil
from poseidon import app
from pyspark.ml.linalg import Vectors
import re
import json

# hdfs client
hdfs_host = app.config.get('HDFS_HOST')
hdfs_user = app.config.get('HDFS_USER')
client = CommonUtil.insecureHdfsClient(hdfs_host, hdfs_user)
# def getListBySql(sql):
#     cursor = CommonUtil.initHiveCursor('default', '', '')
#     return CommonUtil.getHiveSqlResult(cursor, sql)

class Df2csvCom():

    def __init__(self):
        pass

    '''
    tid:the node id
    jobj:options ie attributes of this component
        outpath:the output path of the csv file
    ins is a dict contains:
        in1:xxx   note:df type
    outs is a array contains:
        out1      note:the path of the csv file
    '''

    @staticmethod
    def df2csvComProcesser(tid, jobj, ins, outs, f, *args):
        try:
            f.write('\n#####正在检查df2csv组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())

            res = {}
            # spark initializer
            (conf, spark, sc) = SparkUtil.getSpark()
            comOpts = jobj.get('optsEntity') #user-defined opts
            out_path = app.config.get('DFTOCSV_PATH')
            outpath = comOpts.get('outpath', out_path)

            in1 = ins.get('in1','') # df

            if comOpts:
                CommonUtil.writeDF2CSV(client, in1, outpath)
                f.write('\n数据写入csv文件成功!!!\n')
                if 'out1' in outs:
                    key = '%s:%s' % (tid,'out1')
                    res[key] = 'csv:%s' % outpath
                if not outs:
                    key = '%s:%s' % (tid,'out1')
                    res[key] = 'csv:%s' % outpath
                return res

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0



