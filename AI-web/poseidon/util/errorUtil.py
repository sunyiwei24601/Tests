import os
from flask import Flask
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

import json
from poseidon import app


class MyError(Exception):
    def __init__(self, status):
        if status == 110:
            self.message = 'failed to analyze the task info json'
        elif status == 1001:
            self.message = 'Must specify a output data'
        elif status == 1002:
            self.message = 'Must specify fields of input data'
        elif status == 1003:
            self.message = 'The input table does not existed'
        elif status == 1004:
            self.message = 'The output table has existed'
        elif status == 1005:
            self.message = 'commonopt param must be specified'
        elif status == 1006:
            self.message = 'algopt param must be specified'
        elif status == 1007:
            self.message = 'inputCol must be specified'
        elif status == 1008:
            self.message = 'outputCol must be specified'
        elif status == 1009:
            self.message = 'Must specify the features of the algopt'
        else:
            self.message = 'Unknown error!'
        self.status = status


def riseErrorCode(code):
    abort(code)


@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(MyError)
def MyErrorHandle(error):
    response = dict(status=error.status, message=error.message)
    return jsonify(response), error.status


@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)