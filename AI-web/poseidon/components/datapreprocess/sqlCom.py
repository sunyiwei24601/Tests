'''
process the hive table with sql
'''
# -*- coding: utf-8 -*-
from poseidon.util.commonUtil import CommonUtil
import re

class SQLCom():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
        sql:sql will be written by user(select f1,f2 from ${t1},${t2},${t3},${t4})
    ins is a dict contains:
        in1:xxx   note:the 1th hive table
        in2:xxx   note:the 2th hive table
        in3:xxx   note:the 3th hive table
        in4:xxx   note:the 4th hive table
    outs is an array contains:
        out1
            {
                sql:'select * from table'
                slist:[]
            }
    '''
    @staticmethod
    def SQLComProcesser(tid, jobj, ins, outs, f, *args):
        try:
            f.write('\n#####check params in sqlProcesser in SQLCom:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())

            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts

            sql = comOpts.get('sql','') #get sql specified by user
            in1 = ins.get('in1','') #in1 which is table1 name
            in2 = ins.get('in2','') #in2 which is table2 name
            in3 = ins.get('in3','') #in3 which is table3 name
            in4 = ins.get('in4','') #in4 which is table4 name
            table1 = None
            table2 = None
            table3 = None
            table4 = None
            if in1:
                table1 = in1.split(':')[1]
            if in2:
                table2 = in2.split(':')[1]
            if in3:
                table3 = in3.split(':')[1]
            if in4:
                table4 = in4.split(':')[1]

            #then replace ${t1},${t2},${t3},${t4} with table1,table2,table3,table4 in sql
            sql = SQLCom.replaceWithRelatedTableName(sql,table1,table2,table3,table4)
            f.write('\n$$$$ the real sql after being replaced is below:\n%s'%sql)
            cursor = CommonUtil.initHiveCursor('default', '', '')
            slist = CommonUtil.getHiveSqlResult(cursor, sql)
            f.write('\n$$$$ Grab sql result data done! sqlCom finished!\n')
            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                out1 = {}
                out1['sql'] = sql
                out1['slist'] = slist
                res[key] = out1

            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            f.close()
            return 0
    @staticmethod
    def replaceWithRelatedTableName(sql,table1,table2,table3,table4):
        if table1:
            sql, number  =  re .subn('\$\{t1\}', table1, sql)
        if table2:
            sql, number  =  re .subn('\$\{t2\}', table2, sql)
        if table3:
            sql, number  =  re .subn('\$\{t3\}', table3, sql)
        if table4:
            sql, number  =  re .subn('\$\{t4\}', table4, sql)

        return sql
