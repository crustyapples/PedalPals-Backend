from flask import Flask
from flask_pymongo import PyMongo
from app.models.user import bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config.Config')  # Load configurations from `config.py`
mongo = PyMongo(app)
bcrypt.init_app(app)
jwt = JWTManager(app)



