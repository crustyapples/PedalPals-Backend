from flask import Blueprint, jsonify, request
from app import mongo
from app.models import route
from app.utils.data_gov import get_nearest_pm25_and_weather
from app.controllers import route_controller
from bson import ObjectId
from app.utils.one_maps import get_route
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, get_jwt_header
import datetime
from app.models import user as user_model, social_post as post_model


route_routes = Blueprint('route_routes', __name__)
route_control = route_controller.RouteController()

@route_routes.route('/routes', methods=['GET'])
def get_routes():
    return route_control.find_routes()

@route_routes.route('/get-route', methods=['POST'])
def get_cycling_route():
    data = request.get_json()
    start_address = data.get('start_address')
    end_address = data.get('end_address')
    
    return route_control.get_route(start_address, end_address)

@route_routes.route('/post-route', methods=['POST'])
@jwt_required()
def post_cycle_route():
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    caption = request.json.get('caption')
    route = request.json.get('route')
    timestamp = datetime.datetime.now()

    return route_control.post_route(user, caption, route, timestamp)

@route_routes.route('/get-weather-status/<route_id>', methods=['GET'])
def get_weather_status(route_id):
    # get the route object based on route_id from the Route collection
    return route_control.get_weather_status(route_id)

@route_routes.route('/update-route/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    data = request.json
    route = ROUTES[route_id]  # This is a simple lookup based on index. In a real-world scenario, you'd query the database.
    # Assuming attributes in request data matches the attributes of Route class
    for key, value in data.items():
        setattr(route, key, value)
    return jsonify({"message": "Route updated successfully!"})



