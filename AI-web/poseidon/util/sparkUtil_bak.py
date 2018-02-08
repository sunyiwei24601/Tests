# -*- coding: utf-8 -*-
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from poseidon.util.commonUtil import CommonUtil
import re
from pyspark.sql import DataFrame
from poseidon.components.sourceNTarget.hive2dfCom import HiveToDF
from poseidon import app
from pyspark.sql import Row, Column


import os

class SparkUtil():
    sc = None
    spark = None
    conf = None

    # featuresCol = None
    # labelCol = None

    @staticmethod
    def muti_eva_predictions(algorithm, predictions):
        # Select (prediction, true label) and compute test error
        evaluator = MulticlassClassificationEvaluator(labelCol="indexed", predictionCol="prediction", metricName="accuracy")
        accuracy = evaluator.evaluate(predictions)
        return accuracy

    @staticmethod
    def loadData(spark, sc, fileformat, path, algopt):
        features = algopt.get('featuresCol', "features")
        label = algopt.get('labelCol', "label")
        data = None
        # if the file is a hive table or just a file
        if path[0] == '/':
            if not fileformat:
                fileformat = 'libsvm'
            data = spark.read.format(fileformat).load(path)
        else:
            # this is a hive table
            hive_host = app.config.get('HIVE_HOST')
            hive_port = app.config.get('HIVE_PORT')
            hive_user = app.config.get('HIVE_USER')
            cursor = CommonUtil.initHiveCursor(hive_host, hive_port, hive_user)

            features = CommonUtil.getHiveSqlResult(cursor, "select %s from %s" % (features, path))

            labels = CommonUtil.getHiveSqlResult(cursor, "select %s from %s" % (label, path))

            aa = sc.parallelize(labels)
            aa = aa.map(lambda line: line[0])

            bb = sc.parallelize(features)
            bb = bb.map(lambda line: Vectors.dense(line))

            cc = aa.zip(bb)
            data = spark.createDataFrame(cc, [label, "features"])

        stringIndexer = StringIndexer(inputCol=label, outputCol="indexed")
        si_model = stringIndexer.fit(data)
        td = si_model.transform(data)
        return td

    @staticmethod
    def getSpark():
        if not SparkUtil.spark:

                print('####Initialize spark for first time...')
                os.environ["SPARK_HOME"] = app.config.get('SPARK_HOME')
                PYSPARK_PYTHON = app.config.get('PYSPARK_PATH')
                os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
                app_name = app.config.get('APP_NAME')
                master = app.config.get('MASTER')
                ui_port = app.config.get('UI_PORT')
                dist_files = app.config.get('DIST_FILES')
                executorenv_key = app.config.get('EXECUTORENV_KEY')
                executorenv_value = app.config.get('EXECUTORENV_VALUE')

                SparkUtil.conf = SparkConf().setAppName(app_name).setMaster(master)\
                    .set('spark.ui.port', ui_port)\
                    .set('spark.yarn.dist.files', dist_files)\
                    .setExecutorEnv(executorenv_key,executorenv_value)

                SparkUtil.spark = SparkSession \
                    .builder \
                    .config(conf=SparkUtil.conf) \
                    .enableHiveSupport() \
                    .getOrCreate()
                SparkUtil.sc = SparkUtil.spark.sparkContext
        return (SparkUtil.conf, SparkUtil.spark, SparkUtil.sc)
    '''
    used to vectorize the list in lists generated by sql
    mutiCol_array:['f1,f2','f3,f4']
    oneCol_array:['label','label2']
    after being transformed the result is tuple like below:
        dense vector format:
            (Vectors.dense([f1,f2]),Vectors.dense([f3,f4]),label,label2)
        or
        sparse vector format:
            (Vectors.sparse(2,[0,1],[f1,f2],Vectors.sparse(2,[0,1],[f3,f4],label,label2)

    '''
    @staticmethod
    def sql_res_list_vectorization_method_wrapper(tosparsedata,mutiCols_array,oneCol_array):

        if tosparsedata == '0':
            def dense_vectorize(line):
                # (Vectors.dense([line['library1'],line['library2'],line['library3']]),line['stutas'])
                dense_arrays = []
                for mutiCols in mutiCols_array:
                    if not mutiCols:continue

                    dense_array = []
                    for key in mutiCols.split(','):
                        dense_array.append(line[key])
                    dense_arrays.append(Vectors.dense(dense_array))

                for oneCol in oneCol_array:
                    if not oneCol:continue

                    dense_arrays.append(line[oneCol])

                return tuple(dense_arrays)
                # return (Vectors.dense(dense_array_feature),scalar_label)
            return dense_vectorize
        else:
            def sparse_vectorize(line):
                #(Vectors.sparse(1, [0], [1.0])
                sparse_arrays = []
                for mutiCols in mutiCols_array:
                    if not mutiCols:continue
                    featuresArray = mutiCols.split(',')
                    df_features_size = len(featuresArray)

                    sparse_index_no = df_features_size
                    sparse_index_array = []
                    sparse_value_array = []

                    for i in range(df_features_size):
                        key = featuresArray[i]
                        value = line[key]
                        #if the value is not None,append the key index ie i to sparse_index_array,append the value to sparse_value_array
                        if value:
                            sparse_index_array.append(i)
                            sparse_value_array.append(value)
                    sparse_arrays.append(Vectors.sparse(sparse_index_no,sparse_index_array,sparse_value_array))

                for oneCol in oneCol_array:
                    if not oneCol:continue
                    # scalar_label = line[oneCol]
                    sparse_arrays.append(line[oneCol])

                return tuple(sparse_arrays)
                # return (Vectors.sparse(sparse_index_no,sparse_index_array,sparse_value_array),scalar_label)
            return sparse_vectorize
    '''
    #sql like select f1,f2 from table1,table2,table3, so we need to extract f1,f2 into  [f1,f2],this is the simplest case
    #So when sql is complex, how to extract?
    :param sql:
    :return:
    '''
    @staticmethod
    def extractSQLFields(sql):
        '''
        sql = "select age,"\
        "(case sex when 'male' then 1 else 0 end) as sex,"\
        "(case cp when 'angina' then 0  when 'notang' then 1 else 2 end) as cp,"\
        "trestbps,"\
        "chol,"\
        "(case fbs when 'true' then 1 else 0 end) as fbs,"\
        "(case restecg when 'norm' then 0  when 'abn' then 1 else 2 end) as restecg,"\
        "thalach,"\
        "(case exang when 'true' then 1 else 0 end) as exang,"\
        "oldpeak,"\
        "(case slop when 'up' then 0  when 'flat' then 1 else 2 end) as slop,"\
        "ca,"\
        "(case thal when 'norm' then 0  when 'fix' then 1 else 2 end) as thal,"\
        "(case status  when 'sick' then 1 else 0 end) as ifHealth"\
        "from  ${t1};"
        '''
        sql2, number  =  re .subn('(\([^)]*\))', '', sql) # remove content contained by each (),include ()
        sql3, number  =  re .subn('select', '', sql2) # remove select
        sql4, number  =  re .subn('(from.*)', '', sql3) # remove content after 'from' include 'from'
        sql5, number  =  re .subn(' as', '', sql4) # remove 'as'
        sql6, number  =  re .subn('\s', '', sql5) # remove blank
        return sql6.split(',')
    @staticmethod
    def assembleFieldArray(mutiCol_array,oneCol_array):
        df_fields = []
        if mutiCol_array:
            for mutiCol in mutiCol_array:
                for col in mutiCol.split(','):
                    if col:
                        df_fields.append(col)
        if oneCol_array:
            for oneCol in oneCol_array:
                if oneCol:
                    df_fields.append(oneCol)
        return df_fields

    @staticmethod
    def estimatorDataProcess(tid, jobj, in_data, training_df, f):
        # spark initializer
        (conf, spark, sc) = SparkUtil.getSpark()

        comOpts = jobj.get('optsEntity','')
        #get featuresCol and labelCol from comOpts
        featuresCol = comOpts.get('featuresCol','')
        labelCol = comOpts.get('labelCol','')

        #if convert the data to sparse data
        tosparsedata = comOpts.get('tosparsedata','')

        #if in1 is hive table name like 'default.tablename', then we need to convert it to df type
        #or in1 is a file path in hdfs     and type(in1) != type(DataFrame)
        if type(in_data) == type(u'str'):
            #if in1 is of str type, then we to figure out if it is of hivetable name or libsvm path
            if in_data.find('hivetable:') != -1:
                f.write('\n###########in1 is hive table, now convert it to df type...\n')

                jobj2 = {
                    "optsEntity": {
                        "features": featuresCol,
                        "label": labelCol
                    }
                }
                ins = {'in1':in_data.split(':')[1]}
                outs = ['out1']
                hive2dfComRes = HiveToDF.hive2df(tid,jobj2,ins,outs,f)
                training_df = hive2dfComRes.get('%s:out1' % tid,'')
                # in1.show(truncate=False)
                f.write('\n########### After being transformed,in1 become df type as below:\n %s' % in_data.__str__())
            elif in_data.find('libsvm:')!=-1:
                filetype = in_data.split(':')[0]
                dfspath = in_data.split(':')[1]
                f.write('\n###########in1 is a path of %s file, now read it to df\n' % filetype)
                if filetype == 'libsvm':
                    training_df = spark.read.format("libsvm").load(dfspath)
                    f.write('\n########### After being transformed,in1 become df type as below:\n %s' % in_data.__str__())
        elif type(in_data) == dict:
            sql = in_data.get('sql','')
            if sql:
                f.write('\n###########in1 is dict which contains sql result slist,now grab it out and convert it to df data which contains fields features and label\n')
                # in1 is the result generated by sqlCom, so here we need convert it to df type by sql
                #1. extract fields[f1,f2,...label] from sql(select f1,f2,...label from table)
                sql_fields = SparkUtil.extractSQLFields(sql)
                f.write('\n#######extract fields from sql as below:\n %s' % sql_fields.__str__())
                #2. convert list to df by fields, the num of fields should be equal to the size of the item in list
                sql_df = spark.createDataFrame(in_data.get('slist',''),sql_fields)
                f.write('\n#######convert python list type data slist to df contains fields:\n %s' % sql_fields.__str__())
                #3. assemble the df by featuresCol and labelCol:combine all cols of featuresCol into features, and set labelCol to label.
                #   dynamically get the vectorization method by 'tosparsedata' option specified by user, if it is '1', the method will be
                #   sparse_vectorize which will vectorize the data in a sparse vector, or the method will be dense_vectorize which will vectorize
                #   the data in a dense vector
                vectorization = SparkUtil.sql_res_list_vectorization_method_wrapper(tosparsedata,[featuresCol],[labelCol])
                f.write('\n######get vectorization method by featuresCol and labelCol\n ')
                final_rdd = sql_df.rdd.map(vectorization)
                training_df = spark.createDataFrame(final_rdd,['features','label'])
                f.write('\n######## converting slist to training_df as below:\n%s' % training_df.__str__())
        elif type(in_data) == DataFrame:
            #if this is of df where its head is f1,f2,...,label and the specified featuresCol is f1,f2,...,fn,
            # then we need to assemble the f1,f2,...fn into one column called 'features' in spark, caz the features
            # in spark is a muti-dimensions column and the label is a scalar.
            # func = SparkUtil.generate_AssembleFeaturesNLabelFunc(featuresCol,labelCol)
            # in1 = in_data.rdd.map(func).toDF()
            # training_df = in1
            # training_df.show()
            # return training_df
            feature_list = featuresCol.split(",")
            assembler = VectorAssembler(inputCols=[ feature for feature in feature_list ], outputCol="features")
            training_df = assembler.transform(in_data)
            if labelCol:
                training_df = training_df.withColumnRenamed(labelCol, "label")
            print(">>"*20)
            training_df.show()
            print(">>"*20)
            return training_df

    @staticmethod
    def generate_AssembleFeaturesNLabelFunc(featuresCol,labelCol):
        def assembleFeatures(row):
            #we gonna return the new_row as Row(label=0.0, features=Vectors.dense([0.0, 0.0]))
            new_features = []
            new_label = None
            if featuresCol:
                for feature in featuresCol.split(','):
                    new_features.append(row[feature])
            if labelCol:
                new_label = row[labelCol]
            new_row = Row(label=new_label, features=Vectors.dense(new_features))
            return new_row
        return assembleFeatures