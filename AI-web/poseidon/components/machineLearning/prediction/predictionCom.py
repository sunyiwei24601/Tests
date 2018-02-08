# -*- coding:UTF-8 -*-
from __future__ import print_function
import json

from poseidon.util.commonUtil import CommonUtil
from poseidon.util.sparkUtil import SparkUtil
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame
from poseidon import app

# hdfs client
hdfs_host = app.config.get('HDFS_HOST')
hdfs_user = app.config.get('HDFS_USER')
client = CommonUtil.insecureHdfsClient(hdfs_host, hdfs_user)


class PredictionCom():
    """
    This method is actually a transformer in spark,a spark transformer accept 2 args, one is model and the other one is the data
    is going to be transformed or predicted. One thing to note is the df is a dataframe if the input of the commonopt of the jobj is
    not a hive table, if the input is the hive table, we need to convert the hive table to dataframe.
    If the features of the algopt contains only 1 column, then it is probably the hive table applied to the word2vec model to transformer.
    If the features of the algopt contains more than 2 columns, then we gonna assemble these columns together as a features column and
    convert it to the dataframe.
    """

    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   note:model
        in2:xxx   note:input data which is of df type
    outs is a array contains:
        out1      note:predicted data which is of df type
    '''

    @staticmethod
    def predictionComProcesser(tid, jobj, ins, outs, f, *args):
        try:
            f.write('\n#####正在检查预测组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%json.dumps(jobj))
            f.write('ins:%s\n'%ins.__str__()[:300])
            f.write('outs:%s\n'%outs.__str__()[:300])

            res = {}
            (conf, spark, sc) = SparkUtil.getSpark()
            in1 = ins['in1'] # model
            in2 = ins['in2'] #input data which is of either hive table or df type
            comOpts = jobj.get('optsEntity') #user-defined opts
            #if convert the data to sparse data
            tosparsedata = comOpts.get('tosparsedata','')
            test_df = None # test data
            predictionCol = comOpts.get('predictionCol', "")
            probabilityCol = comOpts.get('probabilityCol', "")

            test_df = PredictionCom.predictorDataProcess(tid, jobj, in2, test_df, f, comOpts)

            (conf, spark, sc) = SparkUtil.getSpark()
            # make a prediction i.e. make a transformation
            predictions = in1.transform(test_df)
            predictions.show()
            print("The information above！！！！！！！")


            # if predictions
            if predictionCol:
                predictions = predictions.withColumnRenamed("prediction", predictionCol)

            if probabilityCol:
                predictions = predictions.withColumnRenamed("probability", probabilityCol)
            f.write('\n#####预测结束！\n')

            # 要保存到的数据库名字
            dbname = app.config.get('INTERMEDIA_HIVE_DB')
            # 要保存到的表名，由用户指定(从前端获取)
            dfname = comOpts.get('dfname', '')
            ifsave = comOpts.get('ifsave', '')
            if ifsave == '1':
                f.write('\n####保存预测结果到%s数据库%s数据表中...\n' % (dbname, dfname))
                predictions.write.saveAsTable('%s.%s' % (dbname, dfname), mode = 'overwrite')
            # test
            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = predictions
            f.write('\n#####预测组件输出如下:\n%s' % res.__str__())
            return res

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0


    @staticmethod
    def predictorDataProcess(tid, jobj, in_data, test_df, f, comOpts):
        # spark initializer
        (conf, spark, sc) = SparkUtil.getSpark()

        comOpts = jobj.get('optsEntity','')
        #get featuresCol, originalCol from comOpts
        featuresCol = comOpts.get('featuresCol','')
        originalCol = comOpts.get('originalCol', "")

        if type(in_data) == type(u'str'):
            #if in1 is of str type, then we to figure out if it is of hivetable name or libsvm path
            if in_data.find('hivetable:') != -1:
                f.write('\n###########第二个输入口输入数据为数据表，正在将其转换为dataframe...\n')

                in_data = spark.sql("select * from %s" % in_data.split(':')[1])

                f.write('\n###########第二个输入口输入数据转换后结果如下:\n %s' % in_data.__str__())
            elif in_data.find('libsvm:')!=-1:
                filetype = in_data.split(':')[0]
                dfspath = in_data.split(':')[1]
                f.write('\n###########第二个输入口输入数据为%s，正在将其加载为dataframe...\n' % filetype)
                if filetype == 'libsvm':
                    training_df = spark.read.format("libsvm").load(dfspath)
                    f.write('\n###########第二个输入口输入数据转换后结果如下:\n %s' % in_data.__str__())

        if type(in_data) == DataFrame:
            #we gonna assemble all features columns to one column called 'features' and keep the original columns
            featuresArray = featuresCol.split(',')
            oriColArray = originalCol.split(',')
            vecAssembler = VectorAssembler(inputCols=featuresArray, outputCol="features")
            in_data = vecAssembler.transform(in_data)

            #得到所有的列
            allCols = in_data.columns
            #保存original columns
            for col in allCols:
                if col!='features' and col not in oriColArray:
                    in_data = in_data.drop(col)
            test_df = in_data
        return test_df
