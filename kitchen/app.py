from flask import Flask
from flask_smorest import Api

from config import BaseConfig

app = Flask(__name__)

kitchen_api = Api(app)
