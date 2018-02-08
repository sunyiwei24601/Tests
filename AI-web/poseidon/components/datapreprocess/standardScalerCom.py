# -*- coding: utf-8 -*-
__author__ = "hand"

import json

from pyspark.ml.feature import StandardScaler
from poseidon.util.sparkUtil import SparkUtil

class StandardScalerCom():

    @staticmethod
    def getStandardScaler(opt):

        standardScaler = StandardScaler(withMean=bool(opt.get('withMean', "False")),
                                        withStd=bool(opt.get('withStd', "True")),
                                        inputCol="features",
                                        outputCol="features_scaled")
        return standardScaler
        # # 用户指定的特征列
        # global feature_list
        # features_col = opt.get('featuresCol')  # 可能为'f1'或者'f1,f2,f3'
        # feature_list = features_col.split(',')
        # assembler = VectorAssembler(inputCols=[feature for feature in feature_list if feature != ''], outputCol="features")
        # training_df = assembler.transform(training_data)  # f1,features,label
        # # 生成标准化工具
        # # 如果只有一列需要标准化
        # if len(feature_list) == 1:
        #     outputCol = features_col+"_scaled"
        #     ss = StandardScaler(withMean=False, withStd=True, inputCol="features", outputCol=outputCol)
        #
        #     return ss,training_df,features_col,outputCol
        # # 多个列需要标准化
        # else:
        #     outputCol = "features_scaled"
        #     ss = StandardScaler(withMean=False, withStd=True, inputCol="features", outputCol=outputCol)
        #     return ss,training_df,features_col,outputCol


    @staticmethod
    def standardScalerComProcesser(tid, jobj, ins, outs, f, *args):
        try:
            f.write('\n#####正在检查标准化组件参数:\n')
            f.write('tid:%s\n' % tid)
            f.write('jobj:%s\n' % json.dumps(jobj))
            f.write('ins:%s\n' % ins.__str__()[:300])
            f.write('outs:%s\n' % outs.__str__()[:300])

            (conf, spark, sc) = SparkUtil.getSpark()

            res = {}
            comOpts = jobj.get('optsEntity', '')
            features_col = comOpts.get('featuresCol')  # 可能为'f1'或者'f1,f2,f3'
            feature_list = features_col.split(',')
            if_save = comOpts.get('if_save', '').lower()  # 获取用户输入是否保存的标记
            training_data = ins.get('in1','')
            model = ins.get('in2','')

            training_df = None
            training_df = SparkUtil.estimatorDataProcess(tid, jobj, training_data,training_df, f)

            standardScaler = StandardScalerCom.getStandardScaler(comOpts)  # 接收标准化处理器和处理后的训练数据
            f.write('\n#####正在生成标准化组件模型...\n')

            if not model:
                f.write('standardScaler model 不存在，现在创建...')
                model = standardScaler.fit(training_df)  # 产生训练模型

            f.write('\n#####正在进行数据标准化转换...\n')
            training_df = model.transform(training_df).drop('features')
            # 获取标准化后的列
            df_scaled = training_df.select("features_scaled")
            #test
            df_scaled.write.parquet("/tmp/df_scaled.parquet")
            rdd = df_scaled.rdd.map(lambda line:tuple(line[0]))
            df = spark.createDataFrame(rdd, feature_list)
            print('recover the df..')
            df.show(2)

            df_columns = df.columns
            for col in df_columns:
                training_df.withColumn(col, df[col])

            # 是否需要保存原列
            if if_save == "n":
                for feature in feature_list:
                    training_df = training_df.drop(feature)

            elif if_save == 'y' or if_save == '':
                pass

            print("&"*20)
            training_df.show()

            if 'out1' in outs:
                key = "{}:{}".format(tid,'out1')
                res[key] = training_df
            if 'out2' in outs:
                key = "{}:{}".format(tid,'out2')
                res[key] = model
            f.write('\n#####数据标准化转换完成！:\n')

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0
