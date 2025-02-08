import json

from flask import Flask
from rmb import rmb

app = Flask(__name__)

app.register_blueprint(rmb)


@app.route('/')
def hello_world():  # put application's code here
    return "hi"

