from flask import Flask
from .main import TwitterHandler


app = Flask(__name__)
twitter = TwitterHandler()


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/ping')
def ping():
    return 'pong'
