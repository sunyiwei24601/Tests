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
from poseidon.util.hive2dfUtil import HiveToDF

# hdfs client
client = CommonUtil.insecureHdfsClient('http://192.168.11.176:50070/', 'jlye')


class StringIndexerCom():
    def __init__(self):
        pass

    @staticmethod
    def getStringIndexer(opt):
        return StringIndexer(inputCol=opt.get('inputCol', None),
                             outputCol=opt.get('outputCol', None),
                             handleInvalid="error")

    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   note:input data which df type
    outs is a array contains:
        out1      note:model
        out2      note:output data after being transformed by model,out2 is of df type
    '''
    @staticmethod
    def stringIndexerTrainer(tid, jobj, ins, outs):

        try:
            res = {}
            (conf, spark, sc) = SparkUtil.getSpark()

            in1 = ins.get('in1','')

            # train stringIndexer input_data get df
            stringIndexer = StringIndexerCom.getStringIndexer(jobj.get('optsEntity'))
            model = stringIndexer.fit(in1)
            # # store the model
            basepath = '/tmp/'
            modelPath = basepath+'poseidon/9-8-si_model'
            # if this path existed,del it
            CommonUtil.delIfExistsInHdfs(client, modelPath)
            model.save(modelPath)
            # transform training data with model
            indexed_data = model.transform(in1)
            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = model
            if 'out2' in outs:
                key = '%s:%s' % (tid,'out2')
                res[key] = indexed_data
            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0




