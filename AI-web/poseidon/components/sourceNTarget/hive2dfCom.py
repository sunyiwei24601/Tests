# -*- coding: utf-8 -*-
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil
from pyspark.ml.linalg import Vectors
import re
import json

# def getListBySql(sql):
#     cursor = CommonUtil.initHiveCursor('default', '', '')
#     return CommonUtil.getHiveSqlResult(cursor, sql)

class HiveToDF():

    def __init__(self):
        pass

    '''
    tid:the node id
    jobj:options ie attributes of this component
    ins is a dict contains:
        in1:xxx   note:input data which is a hive table name
    outs is a array contains:
        out1      note:df type contains dense matrix
        out2      note:df type contains sparse matrix
    '''

    @staticmethod
    def hive2df(tid, jobj, ins, outs, f):
        try:
            f.write('\n#####正在检查HiveToDF组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%json.dumps(jobj))
            f.write('ins:%s\n'%json.dumps(ins))
            f.write('outs:%s\n'%json.dumps(outs))

            res = {}
            # spark initializer
            (conf, spark, sc) = SparkUtil.getSpark()
            '''
           comOpts:{
           'col1':'f1,f2,f3...',
           'col2':'f4,f5,f6...',
           ....
           }
           note: key 'col1' is the column name of df,
                 value 'f1,f2,f3...' is the hive table columns name
           '''
            comOpts = jobj.get('optsEntity') #user-defined opts
            # print(comOpts)

            in1 = ins.get('in1','') # hive table

            multlists = [] # used to store list of muti-columns of df
            final_list = [] #final list used to create df
            df_columns = []  # like ['features','label']
            if comOpts:
                # print(keys)
                for df_column in comOpts:
                    df_columns.append(df_column)
                    #one df column may be mapped to mutiple hive table columns
                    hive_columns = comOpts[df_column]
                    sql = "select {} from {}".format(hive_columns, in1)
                    cursor = CommonUtil.initHiveCursor('default', '', '')
                    mlist = CommonUtil.getHiveSqlResult(cursor, sql)
                    # print('mlist')
                    # print(mlist[0])
                    multlist = []
                    # Note:features must be greater than 1,cause all feature columns will be converted into muti-dimensions vector like [1,2,2,3,...]
                    # If the features contains only one column, then it will be converted into a scalar value
                    if hive_columns.find(',') != -1:
                        for items in mlist:
                            # if the features contains empty value which indicates we need to convert this features into a sparse vector, or we need to convert it to a dense vector
                            # vec = HiveToDF.vectorizeItems(items)
                            array = [Vectors.dense(list(items))]
                            multlist.append(array)
                    else:
                        # value contains only one column
                        for line in mlist:
                            multlist.append([line[0]])
                    # print('multlist')
                    # print(multlist[0])

                    if not multlists:
                        multlists = multlist
                        # print(multlists)
                    else:
                        for i in range(len(multlists)):
                            multlists[i].append(multlist[i][0])
                    # print('multlists')
                    # print(multlists[0])
                #convert the array list to tuple list ie the final_df
                for one in multlists:
                    df_tup = tuple(one)
                    final_list.append(df_tup)
                df = spark.createDataFrame(final_list, df_columns)
                # df.show()
                if 'out1' in outs:
                    key = '%s:%s' % (tid,'out1')
                    res[key] = df
                if 'out2' in outs:
                    key = '%s:%s' % (tid,'out2')
                    res[key] = df
                return res

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0


    @staticmethod
    def vectorizeItems(items):
        for item in items:
            if not item:
                pass
        pass