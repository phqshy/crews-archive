import json

from flask import Flask, Blueprint
from rmb import rmb

app = Flask(__name__)

base_blueprint = Blueprint('api', __name__, url_prefix="/api")
base_blueprint.register_blueprint(rmb)
app.register_blueprint(base_blueprint)


@app.route('/')
def hello_world():  # put application's code here
    print(app.url_map)
    return "hi"

