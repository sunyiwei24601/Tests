
from __future__ import print_function
import json
from flask import  jsonify
import re
import string

from poseidon.util.commonUtil import CommonUtil

from poseidon.util.jiebaUtil import JiebaUtil
#hdfs client
client = CommonUtil.insecureHdfsClient('http://dasrv03.novalocal:50070/','glzheng')


class TokenizerService():

    @staticmethod
    def jieba_tokenizer(jobj):
        try:
            tokenizer_opt = jobj.get('tokenizer_opt', "") # tokenizer_opt args
            commonopt = jobj.get('commonopt', "") # common args
            if tokenizer_opt:
                #stop words
                stops = tokenizer_opt.get('stops', ["/storeage/glzheng/qingbaodata/jieba_stops.txt"])
                #custom files
                dicts = tokenizer_opt.get('dicts', ["/storeage/glzheng/qingbaodata/negative.txt","/storeage/glzheng/qingbaodata/positive.txt"])
                JiebaUtil.loadUserDic(dicts,stops)

            if commonopt:
                #file is going to be tokenized
                in_path = commonopt.get('in_path')
                #file after being tokenized
                out_path = commonopt.get('out_path')
                #file after being tokenized
                fields = commonopt.get('fields')

                if not in_path:
                    return 1000
                if not out_path:
                    return 1001
                if not fields:
                    return 1002

                cursor = CommonUtil.initHiveCursor('default','','')
                #check if the in_path exists
                res = CommonUtil.findTablesInPath(cursor,in_path)
                if not res:
                    return 1003
                #check if the out_path exists
                res = CommonUtil.findTablesInPath(cursor,out_path)
                if res:
                    return 1004

                #get desc of hive table
                desc = CommonUtil.getDescByHiveTable(cursor,in_path)
                #create new table by the desc of last step
                CommonUtil.createHiveTableWithSerDe(cursor,out_path,desc,'csv')

                #read the input file from hive
                # hsql = "select %s from %s"%(fields,in_path)
                hsql = "select * from %s" % in_path
                lines = CommonUtil.getHiveSqlResult(cursor,hsql)

                #get table heads like ['1','2','3']
                t_heads = CommonUtil.getHiveTableHead(cursor,in_path)
                #get fields which is going to be tokenized
                t_fields = fields.split(',')

                #find the index of each t_fields in the t_heads
                indices = []
                for t_field in t_fields:
                    indices.append(t_heads.index(t_field))

                #write into a csv file
                csv_content = []
                for cols in lines:
                    csv_line = list(cols)
                    for index in indices:
                        csv_line[index] = JiebaUtil.tokenizewithjieba(cols[index]).encode('utf-8')
                    csv_content.append(csv_line)

                CommonUtil.writeList2CSV(client,csv_content,'/tmp/test.csv')
                CommonUtil.loadFile2HiveSerDeTable(cursor,'/tmp/test.csv',out_path)
                return 1
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0
















