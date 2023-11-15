from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os

app = Flask(__name__)
app.config.from_object('app.config.Config')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

def register_blueprints():
    from app.routes.user_routes import user_routes
    from app.routes.social_routes import social_routes
    from app.routes.route_routes import route_routes
    from app.routes.google_maps_routes import google_maps_routes
    from app.routes.gamification_routes import gamification_routes
    
    app.register_blueprint(user_routes)
    app.register_blueprint(route_routes)
    app.register_blueprint(social_routes)
    app.register_blueprint(google_maps_routes)
    app.register_blueprint(gamification_routes)

register_blueprints()
