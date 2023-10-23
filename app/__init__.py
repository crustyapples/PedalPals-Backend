from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config.Config')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def register_blueprints():
    from app.routes.user_routes import user_routes
    from app.routes.social_routes import social_routes
    from app.routes.route_routes import route_routes
    
    app.register_blueprint(user_routes)
    app.register_blueprint(route_routes)
    app.register_blueprint(social_routes)

register_blueprints()
