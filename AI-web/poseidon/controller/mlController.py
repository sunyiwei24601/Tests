# -*- coding: utf-8 -*-

from flask import request
import json
import os
import subprocess

from poseidon.util.errorUtil import auth

from poseidon import app

from poseidon.util.errorUtil import MyError
from poseidon.util.commonUtil import CommonUtil
from poseidon.components.sourceNTarget.hive2dfCom import HiveToDF
from poseidon.coordinator.taskAnalyzer import TaskAnalyzer
from poseidon.coordinator.coordinator import Coordinator
from poseidon.util.aiTaskLog import AITaskLog
from poseidon.coordinator.taskCleaner import TaskCleaner
from poseidon.util.mysqlUtil import MySQLUtil

# test
# curl -i -H "Content-Type: application/json" -X POST -d '
# {"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
# windows: curl -i -H "Content-Type: application/json"
#  -X POST -d "{"""title""":"""Read a book"""}" http://localhost:5000/todo/api/v1.0/task

@app.route('/tasks/test', methods=['POST'])
def taskTest():
    try:
        print(json.dumps(request.json))
        #clear the correspond log roller
        AITaskLog.logRoller = {}

        #get log base path in the settings file
        log_dir = app.config.get('LOG_DIR')

        username = request.json.get('userName','unknown-user')
        taskname = request.json.get('taskName','unknown-task')
        taskTime = str(request.json.get('taskTime','unknown-time'))

        #tasks/username-taskname-taskTime.log
        filename = '%s/%s-%s-%s.log' % (log_dir, username,taskname,taskTime)

        #del by the log pattern
        pattern = '%s-%s-\\d{13}.log' % (username,taskname)
        CommonUtil.delByRegex(log_dir,pattern)

        # kafka_settings = {
        #         'bootstrap_servers':'192.168.11.190:6667',
        #         'topic':'ai-%s-%s' % (TaskAnalyzer.userid,TaskAnalyzer.taskid)
        # }
        # f = AITaskLog(filename,kafka_settings)

        f = AITaskLog(filename,None)
        f.write('\n#### 解析 graph json...\n')

        res = TaskAnalyzer.analyzeGraphJson(request.json)

        if res == 0:
            raise MyError(123)
        taskJson = TaskAnalyzer.nodesTaskInfo
        f.write('\n#### 完成解析 graph json 如下:\n')
        f.write(json.dumps(taskJson))
        f.write('\n#### 执行节点...\n')
        Coordinator.executeNodes(taskJson,f,username,taskname)
        res = Coordinator.global_result_vars
        return res.get('flag')
    except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0
    finally:
        #wait for kafka producer sending all messages done
        f.kafka_flush()
        f.close()
        #clear all global vars of TaskAnalyzer in order to run the next task initially
        TaskCleaner.cleanTask()

'''
grab the logcontent by logname
'''
@app.route('/tasks/logcontent', methods=['POST'])
def logcontent():
    #username-taskname-tasktime.log
    filename = request.json.get('filename','')
    if not filename:
        print('WTF! filename is empty')
    logroller = AITaskLog.logRoller.get(filename,'')

    print('logcontent come')
    return logroller
import sys



'''
grab the logcontent by logname
'''
@app.route('/tasks/nodecontent', methods=['POST'])
def nodecontent():
    content = ''
    #username-taskname-tasktime.log
    filename = request.json.get('filename','')
    if not filename:
        print('WTF! filename is empty')
    #if logroller is empty, then maybe this request comes from '查看日志' of the right click menu of one node, if so, the filename
    # does not contains the tasktime
    logdir = app.config.get('LOG_DIR')
    for root, dirs, files in os.walk(logdir, topdown=False):
        for name in files:
            if filename[:-4] == name[:-18]:
                f = open('%s/%s' % (logdir,name))
                content = f.read()
                f.close()
    return content


@app.route('/tasks/deltask', methods=['POST'])
def deltask():
    """
    删除任务后清空对应日志、模型、数据库中的路径
    :return:
    """
    try:
        username = request.json.get('userName', 'unknown-user')
        taskname = request.json.get('taskName', 'unknown-task')
        # 获取日志文件的路径
        log_dir = app.config.get('LOG_DIR')
        # 根据正则找到日志后删除
        pattern = '%s-%s-\\d{13}.log' % (username, taskname)
        CommonUtil.delByRegex(log_dir, pattern)

        # 删除hdfs上对应任务的模型
        task_dir = app.config.get('TASK_DIR')
        model_path = '%s/%s/%s' % (task_dir, username, taskname)
        subprocess.call(["hdfs", "dfs", "-rm", "-r", model_path])

        # 删除数据库中存储的路径
        db = MySQLUtil.createCursor(app.config.get('MYSQL_HOST'), app.config.get('MYSQL_USER'),
                                    app.config.get('MYSQL_PASSWD'), app.config.get('MYSQL_DB'))
        delsql = "delete from tb_ai_models where task_name = '%s' and user_name = '%s'" % (taskname, username)
        MySQLUtil.exe_update_sql(db, delsql)
    except Exception as e:
        print("*****************Sorry:\n %s" % e)
        return "fail"
    else:
        return "success"


@app.route('/tasks/hive2df', methods=['GET'])
def taskHive2DF():
    jobj = {
                    "optsEntity": {
                        "df1": "f1,f2,f3",
                        "df2": "f4,f5",
                        "label": "label"
                    },
                    "comName": "randomForest",
                    "comCode": "randomForestCom"
                }
    ins = {'in1':'default.sample_svm_data'}
    outs = ['out1']
    code = HiveToDF.hive2df('1111',jobj,ins,outs)
    return CommonUtil.getResultByCode(code)

@app.route('/test/<string:xxx>', methods=['GET'])
def get_task(xxx):
    if xxx != 'hello':
        raise MyError(000)
    # if not request.json or not 'title' in request.json:
    #     raise MyError(111)
    #     pass
    return 'hello'

@app.route('/test/auth', methods=['GET'])
@auth.login_required
def testauth():
    return 'auto successfully!'