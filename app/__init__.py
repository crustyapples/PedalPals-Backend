from flask import Flask
from flask_pymongo import PyMongo
from app.routes import user_routes, route_routes, social_routes
from app.models.user import bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config.Config')  # Load configurations from `config.py`
mongo = PyMongo(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(route_routes, url_prefix='/routes')
app.register_blueprint(social_routes, url_prefix='/social')




