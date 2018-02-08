# -*- coding: utf-8 -*-
__author__ = "hand"

import json
from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil
from pyspark.ml.clustering import KMeans

'''
tid:the node id
jobj:options i.e. attributes of this component
ins is a dict contains:
    in1:xxx   note:training data
outs is a array contains:
    out1      note:clustered data which is of df type
    out2      note:K-means model
'''
class KmeansClusterCom():
    def __int__(self):
        pass

    @staticmethod
    def getKMeansCluster(opt):
        km = KMeans(featuresCol="features",
                                predictionCol="prediction",
                                k=int(opt.get('k', 2)),
                                initMode=opt.get('initMode', "k-means||"),
                                initSteps=int(opt.get('initSteps', 5)),
                                tol=float(opt.get('tol', 1e-4)),
                                maxIter=int(opt.get('maxIter', 20))
                                )
        seed = opt.get('seed', None)

        if seed.strip():
            km = km.setSeed(int(seed))
        else:
            km = km.setSeed(None)  # 如果用户不输入或输入空格
        return km

    @staticmethod
    def kmeansClusterComProcesser(tid, jobj, ins, outs, f,username,taskname):

        try:
            f.write('\n正在检查K-means组件的参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%json.dumps(jobj))
            f.write('ins:%s\n'%ins.__str__()[:200])
            f.write('outs:%s\n'%json.dumps(outs))

            res = {}
            training_df = None
            comOpts = jobj.get('optsEntity','')

            #get featuresCol from comOpts
            featuresCol = comOpts.get('featuresCol','')

            training_df = SparkUtil.estimatorDataProcess(tid, jobj, ins.get('in1',''), training_df, f)
            # km cluster
            f.write('\n#####创建KMeansCluster ...\n')
            km = KmeansClusterCom.getKMeansCluster(comOpts)

            f.write('\n#####正在生成模型...\n')
            model = km.fit(training_df)

            #save model and model path record
            CommonUtil.saveModelNPath(username,taskname,'KMeansModel', model, f)
            if 'out1' in outs:
                clustered_df = model.transform(training_df)
                key = '%s:%s' % (tid,'out1')
                res[key] = clustered_df
            if 'out2' in outs:
                key = '%s:%s' % (tid,'out2')
                res[key] = model
            f.write('\n#####K-means组件输出如下:\n%s' % res.__str__()[:200])
            return res

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0

