# -*- coding: utf-8 -*-
'''
fill na with specified value
'''
from poseidon.util.sparkUtil import SparkUtil
from poseidon import app
import json
from pyspark.sql import DataFrame

class NaFillerCom():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
        filljson:json obj like {col1:val1,col2:val2}
        ifsave: if save the result or not
        dfname: the name of result ie the df
    ins is a dict contains:
        in1:xxx   note:hive table, csv, json, df name, df...
    outs
        out1:df
    '''
    @staticmethod
    def naFillerComProcesser(tid, jobj, ins, outs,f, username, taskname):
        try:
            f.write('\n#####正在检查缺失值填补组件的参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())

            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts

            filljson = comOpts.get('filljson','') #json obj
            ifsave = comOpts.get('ifsave','')
            dfname = comOpts.get('dfname','') #the res of the result
            in1 = ins.get('in1','') #in1 which is table1 name or dfname
            # print('%s+%s+%s+%s' % (filljson, ifsave,dfname,in1))

            (conf, spark, sc) = SparkUtil.getSpark()

            df = None
            #if in1 is a hive table or csv or json or sth, we need to load it with spark sql
            #if in1 is of df type, then go on
            if type(in1) == type(u'str'):
                #if in1 is of str type, then we need to figure out if it is of hivetable name or libsvm path
                if in1.find('hivetable:') != -1:
                    tablename = in1.split(':')[1]
                    df = spark.sql('select * from %s' % tablename)
                elif in1.find('csv:') != -1:
                    pass
            elif type(in1) == DataFrame:
                df = in1

            #judge if the filljson can be converted to a json
            fillr = None
            try:
                fillr = json.loads(filljson)
            except Exception as e:
                fillr = filljson
            f.write('\n$$$$ 用%s填充缺失值...' % fillr.__str__())
            new_df = df.na.fill(fillr)
            f.write('\n$$$$ 缺失值填充完成！')

            # register df to be the temporary table so that it can be handled by next SSQL com
            f.write('\n$$$$保存临时%s数据表' % dfname)
            new_df.createOrReplaceTempView(dfname)
            # new_df.show()

            #save the intermedia if the option 'ifsave' is '1'
            dbname = app.config.get('INTERMEDIA_HIVE_DB')
            if ifsave == '1':
                f.write('\n$$$$ 保存新的dataframe到%s数据库的%s数据表' % (dbname, dfname))
                new_df.write.saveAsTable('%s.%s' % (dbname, dfname), mode = 'overwrite')

            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = 'dfname:%s' % dfname
            if 'out2' in outs:
                key = '%s:%s' % (tid,'out2')
                res[key] = new_df

            f.write('\n#####缺失值填补组件输出如下:\n%s' % res.__str__()[:200])
            return res
        except Exception as e:
            print("\n*****************Sorry:\n %s" % e)
            f.write("\n*****************Sorry:\n %s" % e.message)
            # f.close()
            return 0
