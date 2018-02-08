# -*- coding: utf-8 -*-
import random
import os

from flask import jsonify
from hdfs import InsecureClient
from pyhive import hive
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hive_service import ThriftHive
import xlrd
import time
from poseidon.util.mysqlUtil import MySQLUtil
from poseidon import app
import shutil
import json
import re


class CommonUtil():


    @staticmethod
    def getResultByCode(code):
        result = 'ok'
        if code == 0:
            result = 'ko'
        return jsonify({'result': result}), 201

    @staticmethod
    def insecureHdfsClient(url,user):
        #test setting file
        hdfs_client_url = app.config.get('HADOOP_CLIENT_URL')
        # ('http://dasrv03.novalocal:50070/','glzheng')
        if url == 'default' or user == 'default':
            # url = 'http://dasrv03.novalocal:50070/'
            url = hdfs_client_url
            user = app.config.get('INSECUREHDS_CLIENT_NAME')
        client = InsecureClient(url, user=user)
        return client

    @staticmethod
    def delIfExistsInHdfs(client, hdfspath):
        if client.status(hdfspath, strict=False):
            client.delete(hdfspath, recursive=True)

    @staticmethod
    def delFileIfExists(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def delDirIfExists(dirpath):
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)

    #del the files under the specified dir by regex formula
    @staticmethod
    def delByRegex(file_dir,pattern):
        for root, dirs, files in os.walk(file_dir):
            for filename in files:
                res = re.match(pattern, filename, flags=0)
                filepath = '%s/%s' % (root, filename)
                # if this file match the pattern and this file exists,then del it
                if res and res.group(0) == filename and os.path.exists(filepath):
                    os.remove(filepath)

    @staticmethod
    def initHiveCursor(host, port, user):
        # "192.168.11.189", 10000, "hadoop"
        if host == 'default' or user == 'default' or port == 'default':
            host = app.config.get('HIVE_HOST')
            port = app.config.get('HIVE_PORT')
            user = app.config.get('HIVE_USER')
        # print('%s:%s:%s' % (host,port,user))
        conn = hive.Connection(host=host, port=port, username=user)
        cursor = conn.cursor()
        return cursor

    @staticmethod
    def exeSQLWithHiveClient(host,port,sql):
        # "192.168.11.189", 10000, "hadoop"
        if host == 'default' or port == 'default':
            host = app.config.get('HIVE_HOST')
            port = app.config.get('HIVE_PORT')
        transport = TSocket.TSocket(host, port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        client = ThriftHive.Client(protocol)
        transport.open()

        client.execute(sql)
        transport.close()

    @staticmethod
    def getHiveSqlResult(cursor, sql):
        cursor.execute(sql)
        return cursor.fetchall()

    # @staticmethod
    # def getHiveSqlResult(sql):
    #     cursor = CommonUtil.initHiveCursor('default','','')
    #     cursor.execute(sql)
    #     return cursor.fetchall()

    @staticmethod
    def getDescByHiveTable(cursor,tablename):
        #format:[('id', 'bigint', 'null'), ('real_name', 'string', 'null')]
        descsql = 'desc %s' % tablename
        desctup = CommonUtil.getHiveSqlResult(cursor,descsql)
        desc = ''
        for item in desctup:
            desc += item[0]+" "+item[1]+","
        return desc[0:len(desc)-1]

    @staticmethod
    def getHiveTableHead(cursor, tablename):
        # format:[('id', 'bigint', 'null'), ('real_name', 'string', 'null')]
        descsql = 'desc %s' % tablename
        desctup = CommonUtil.getHiveSqlResult(cursor, descsql)
        desc = ''
        res = []
        for item in desctup:
            res.append(item[0])
        return res

    @staticmethod
    def createHiveTableWithSerDe(cursor,tablename,desc,fformat):
        if fformat == 'csv':
            sql = "CREATE TABLE %s ("\
                "%s )"\
                  " ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'"\
                  " WITH SERDEPROPERTIES ('separatorChar' = ',','quoteChar' = '\"')  "\
                  " STORED AS TEXTFILE" %(tablename,desc)
        elif fformat == 'json':
            sql = "CREATE TABLE %s ("\
                "%s )"\
                  " ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'"\
                  " STORED AS TEXTFILE" %(tablename,desc)
        cursor.execute(sql)

    @staticmethod
    def loadFile2HiveSerDeTable(cursor,inpath,tablename):
        sql = "LOAD DATA INPATH '%s' OVERWRITE INTO TABLE %s" % (inpath,tablename)
        # print(sql)
        cursor.execute(sql)

    @staticmethod
    def findTablesInPath(cursor,path):
        index = path.find('.')
        table = path[index+1:]
        sql = "show tables like '%s'" % table
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @staticmethod
    def writeList2CSV(client,list,filepath):
        CommonUtil.delIfExistsInHdfs(client,filepath)
        with client.write(filepath) as writer:
            for items in list:
                line = ''
                for item in items:
                    line += "\""+item+"\","
                writer.write(line+"\n")
    @staticmethod
    def writeDF2CSV(client,df,filepath):
        CommonUtil.delIfExistsInHdfs(client,filepath)

        list = df.collect()
        columns = df.columns
        csv_head = ''
        for column in columns:
            csv_head += column+','
        csv_head = csv_head[:-1]
        with client.write(filepath) as writer:
            writer.write(csv_head+"\n")
            for items in list:
                line = ''
                for item in items:
                    line += "\""+item.__str__()+"\","
                writer.write(line+"\n")

    @staticmethod
    def generateRandomStr():
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        sa = []
        for i in range(10):
           sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt


    '''
    inpath:local path excel file
        note:the last column must be label column and all the other columns are feature columns
    outpath:hdfs path of libsvm file is going to be generated
        labeled_outpath:records have label
        unlabeled_outpath:records have not label, but we set the label to the default value 110, if
                          have no unlabeled data, this file will be empty.
    labelIndex:label index
        format:real-number
    featuresIndex:features index
        format:[1,2]
    '''
    @staticmethod
    def excel2libsvm(inpath,sheetIndex,labeled_outpath, unlabeled_outpath):

        try:
            client = CommonUtil.insecureHdfsClient('default','default')

            CommonUtil.delIfExistsInHdfs(client,labeled_outpath)
            CommonUtil.delIfExistsInHdfs(client,unlabeled_outpath)
            with client.write(labeled_outpath) as labeled_out,client.write(unlabeled_outpath) as unlabeled_out:
                data = xlrd.open_workbook(inpath)
                # labeled_out = open(labeled_outpath, 'w')
                # unlabeled_out = open(unlabeled_outpath, 'w')
                table = data.sheets()[sheetIndex]
                nrows = table.nrows #行数
                for x in range(nrows):
                    row =table.row_values(x)
                    labelstr = str(row[-1])
                    featuresstr = ''

                    for i in range(len(row)-1):
                        if str(row[i]) == '':
                            continue
                        featuresstr += str(i+1)+':'+str(row[i])+' '

                    if labelstr == '':
                        labelstr = str(110)
                        line = labelstr+' '+featuresstr
                        #write line into the libsvm file
                        unlabeled_out.write(line+'\n')
                    else:
                        line = labelstr+' '+featuresstr
                        #write line into the libsvm file
                        labeled_out.write(line+'\n')
            return 1 #indicates success
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0

    @staticmethod
    def getCurrentTimeStr(fmt):
        if not fmt:
            fmt='%Y%m%d%H%M%S'      #格式化时间
        #Python 获取时间戳
        #Python 默认获取的时间是一个具有时间的元组，asctime()  是接受时间元祖，返回一个时间字符串
        TimeTuple=time.localtime(time.time())   #获取当前的时间返回一个时间元组
        res=time.strftime(fmt,TimeTuple)       #把传入的元组按照格式，输出字符串
        return res

    @staticmethod
    def saveModelNPath(username,taskname, algorithm, model, f):
        try:
            # store model in hdfs and model_path in mysql
            task_dir = app.config.get('TASK_DIR')
            # model_dir = '/tmp/'
            model_path = '%s/%s/%s/models/%s' % (task_dir,username,taskname,algorithm)

            # if this path existed,del it
            # hdfs client
            client = CommonUtil.insecureHdfsClient('default', 'default')
            # CommonUtil.delIfExistsInHdfs(client, model_path)
            model.write().overwrite().save(model_path)
            f.write('\n#####保存%s模型到%s\n' % (algorithm,model_path))

            # model_name = '%s-%s' % (algorithm,CommonUtil.getCurrentTimeStr(''))
            db = MySQLUtil.createCursor(app.config.get('MYSQL_HOST'),app.config.get('MYSQL_USER'),app.config.get('MYSQL_PASSWD'),app.config.get('MYSQL_DB'))
            delsql = "delete from tb_ai_models where task_name = '%s' and user_name = '%s'" % (taskname,username)
            # print(delsql)
            MySQLUtil.exe_update_sql(db,delsql)

            model_opts = {
                "model_path":model_path
            }
            sql = "insert into tb_ai_models (model_name,model_type,model_path,user_name,task_name,com_code,com_name,model_opts) " \
                  "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (algorithm,'task',model_path,username,taskname,'modelCom','modelCom',json.dumps(model_opts))
            # print(sql)
            result = MySQLUtil.exe_update_sql(db,sql)

            db.close()
            f.write('SQL语句执行成功:\n%s' % sql)
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            f.close()
            return 0
