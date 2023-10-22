from flask import Blueprint, jsonify, request
from app import db
from app.models import route

route_routes = Blueprint('route_routes', __name__)

@route_routes.route('/create-route', methods=['POST'])
def create_route():
    data = request.json
    new_route = route_model.Route(**data)
    ROUTES.append(new_route)
    return jsonify({"message": "Route created successfully!"}), 201

@route_routes.route('/update-route/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    data = request.json
    route = ROUTES[route_id]  # This is a simple lookup based on index. In a real-world scenario, you'd query the database.
    # Assuming attributes in request data matches the attributes of Route class
    for key, value in data.items():
        setattr(route, key, value)
    return jsonify({"message": "Route updated successfully!"})

@route_routes.route('/get-route/<int:route_id>', methods=['GET'])
def get_route(route_id):
    route = ROUTES[route_id]
    return jsonify(vars(route))

@route_routes.route('/delete-route/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    del ROUTES[route_id]
    return jsonify({"message": "Route deleted successfully!"})

@route_routes.route('/list-routes', methods=['GET'])
def list_routes():
    return jsonify([vars(route) for route in ROUTES])

@route_routes.route('/get-route-status/<int:route_id>', methods=['GET'])
def get_route_status(route_id):
    route = ROUTES[route_id]
    return jsonify({"route_status": route.getRouteStatus()})

@route_routes.route('/get-weather-status/<int:route_id>', methods=['GET'])
def get_weather_status(route_id):
    route = ROUTES[route_id]
    return jsonify({"weather_status": route.getWeatherStatus()})

@route_routes.route('/get-traffic-info/<int:route_id>', methods=['GET'])
def get_traffic_info(route_id):
    route = ROUTES[route_id]
    return jsonify({"traffic_info": route.getTrafficInfo()})

@route_routes.route('/get-route-difficulty/<int:route_id>', methods=['GET'])
def get_route_difficulty(route_id):
    route = ROUTES[route_id]
    return jsonify({"route_difficulty": route.getRouteDifficulty()})
