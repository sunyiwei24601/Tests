# -*- coding:UTF-8 -*-

from __future__ import print_function
import json

from pyspark.ml.classification import RandomForestClassifier

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

# hdfs client
client = CommonUtil.insecureHdfsClient('default', 'default')

class RandomForestCom():
    @staticmethod
    def getRandomForestClassifier(opt):
        rf = RandomForestClassifier(featuresCol="features",
                                    labelCol="label",
                                    predictionCol=opt.get('predictionCol', "prediction"),
                                    probabilityCol=opt.get('probabilityCol', "probability"),
                                    rawPredictionCol=opt.get('rawPredictionCol', "rawPrediction"),
                                    maxDepth=int(opt.get('maxDepth', 5)),
                                    maxBins=int(opt.get('maxBins', 32)),
                                    minInstancesPerNode=int(opt.get('minInstancesPerNode', 1)),
                                    minInfoGain=float(opt.get('minInfoGain', 0.0)),
                                    maxMemoryInMB=int(opt.get('maxMemoryInMB', 256)),
                                    cacheNodeIds=opt.get('cacheNodeIds', False),
                                    checkpointInterval=int(opt.get('checkpointInterval', 10)),
                                    impurity=opt.get('impurity', "gini"),
                                    numTrees=int(opt.get('numTrees', 20)),
                                    featureSubsetStrategy=opt.get('featureSubsetStrategy', "auto"),
                                    seed=opt.get('seed', None))
        return rf

    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   note:input data which df type
    outs is a array contains:
        out1      note:model
    '''
    @staticmethod
    def randomForestComProcesser(tid, jobj, ins, outs, f,username,taskname):

        try:
            f.write('\n#####正在检查随机森林组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%json.dumps(jobj))
            f.write('ins:%s\n'%ins.__str__()[:200])
            f.write('outs:%s\n'%json.dumps(outs))

            res = {}
            training_df = None
            comOpts = jobj.get('optsEntity','')
            training_df = SparkUtil.estimatorDataProcess(tid, jobj, ins.get('in1',''),training_df, f)
            # rf classifier
            f.write('\n#####正在生成随机森林分类器...\n')
            rf = RandomForestCom.getRandomForestClassifier(comOpts)

            f.write('\n#####正在训练随机森林分类器...\n')
            model = rf.fit(training_df)
            f.write('\n#####模型树如下: \n%s' % model.toDebugString)

            #save model and model path record
            CommonUtil.saveModelNPath(username,taskname,'RandomForestClassificationModel', model, f)
            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = model
            f.write('\n#####随机森林分类器组件输出如下:\n%s' % res.__str__()[:200])
            return res

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0


