# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from flask import jsonify
import re
import string
import numpy as np

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import Word2Vec

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil

#hdfs client
client = CommonUtil.insecureHdfsClient('http://dasrv03.novalocal:50070/','glzheng')


class TestCom():

    @staticmethod
    def test(jobj):

        #store the word2vec
        basepath = '/tmp/'
        word2vecPath = basepath+'poseidon/result'

        loadedWord2Vec = Word2Vec.load(word2vecPath)
        print(loadedWord2Vec.getVectorSize())





