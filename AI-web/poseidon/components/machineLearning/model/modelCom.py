# -*- coding: utf-8 -*-
'''
generate a model by its option:modelpath
'''
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.clustering import KMeansModel
from poseidon.util.sparkUtil import SparkUtil

class ModelCom():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
        optsEntity:
            model_path:the path of hdfs in which the model was stored
    outs
        out1:model
    '''
    @staticmethod
    def modelComProcesser(tid, jobj, ins, outs,f, username, taskname):
        try:
            f.write('\n#####正在检查模型:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())

            (conf, spark, sc) = SparkUtil.getSpark()
            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts

            model_path = comOpts.get('model_path','') #the path of hdfs in which the model was stored
            f.write('\n model path is:\n%s' % model_path)

            #load the model by model_path
            #1.get the class name of the model by model_path
            class_name = model_path.split('/')[-1]
            f.write('\n 准备加载%s模型' % class_name)
            #2.load the model with class_name
            exe_str = '%s.load("%s")' % (class_name,model_path)
            f.write('\n 从:\n%s加载模型成功' % model_path)
            model = eval(exe_str)

            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = model

            f.write('\n#####模型输出如下:\n%s' % res.__str__()[:200])
            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0

