# -*- coding: utf-8 -*-
from flask import Flask
import os

#创建项目对象
app = Flask(__name__)

#import  os
#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')

#加载配置文件内容
app.config.from_object('poseidon.setting')     #模块下的setting文件名，不用加py后缀
# os.environ["FLASKR_SETTINGS"] = "/storeage/glzheng/windowspy/flask_poseidon/poseidon/setting.py"
# app.config.from_envvar('FLASKR_SETTINGS')   #环境变量，指向配置文件setting的路径


from poseidon.controller import mlController
from poseidon.controller import taController
