import os
from flask import Flask, jsonify
from flask import request
from flask import url_for
import json

from poseidon.util.errorUtil import auth

from poseidon import app
from poseidon.service.aiService import AIService

from poseidon.util.commonUtil import CommonUtil

from poseidon.util.errorUtil import MyError, MyErrorHandle

# curl -i -H "Content-Type: application/json" -X POST -d '
# {"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
# windows: curl -i -H "Content-Type: application/json" -X POST -d
# "{"""title""":"""Read a book"""}" http://localhost:5000/todo/api/v1.0/task

@app.route('/textAnalysis/<string:action>', methods=['POST'])
def textAnalysis(action):
    res = AIService.doTextAnalysisAction(action, request.json)
    if type(1) == type(res) and res >= 1000:
        raise MyError(res)
    return CommonUtil.getResultByCode(res)
