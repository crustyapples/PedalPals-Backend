from flask import Blueprint, jsonify, request
from app import db
from app.models import route

route_routes = Blueprint('route_routes', __name__)

@route_routes.route('/routes', methods=['GET'])
def get_routes():
    routes = db.routes.find()
    return jsonify([route for route in routes])

@route_routes.route('/routes/<int:route_id>', methods=['GET'])
def get_single_route(route_id):
    route = db.routes.find_one({"_id": route_id})
    return jsonify(route)

# ... other CRUD operations ...
