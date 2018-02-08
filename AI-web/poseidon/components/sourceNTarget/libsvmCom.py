# -*- coding: utf-8 -*-
'''
specify the libsvm file path as a data source, so this class is simple
'''
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil

class LibsvmCom():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
    outs is a array contains:
        out1      return path of libsvm file
        out2      return df data of out1 file
    '''
    @staticmethod
    def libsvmComProcesser(tid, jobj, ins, outs, f, *args):
        try:
            (conf, spark, sc) = SparkUtil.getSpark()

            f.write('\n#####正在检查libsvm文件组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())
            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts
            dfspath = comOpts.get('dfspath','')

            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = 'libsvm:%s' % dfspath
            if 'out2' in outs:
                key = '%s:%s' % (tid,'out2')
                res[key] = spark.read.format("libsvm").load(dfspath)
            f.write('\n#####libsvm文件组件输出为:\n%s' % res.__str__())
            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0



