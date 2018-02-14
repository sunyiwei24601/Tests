from flask import Flask,url_for

app=Flask(__name__)


@app.route('/<username>')
def hello_world(username):
    return url_for('login')

@app.route('/login')
def login():pass

app.run(debug=True)