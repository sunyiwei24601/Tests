# -*- coding: utf-8 -*-
'''
specify the table as a data source, so this class is simple
'''
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil

class HiveTable():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   specify a hive table as data source
    outs is a array contains:
        out1      return hive table name like default.testTable
    '''
    @staticmethod
    def hiveTableProcesser(tid, jobj, ins, outs, f, *args):
        try:
            f.write('\n#####正在检查hiveTable组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())

            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts
            dbname = comOpts.get('dbname','')
            tablename = comOpts.get('tablename','')

            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = 'hivetable:%s.%s' % (dbname,tablename)
            f.write('\n#####hiveTable输出如下:\n%s' % res.__str__())
            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0



