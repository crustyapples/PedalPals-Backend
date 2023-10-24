from app import mongo
from app.utils.one_maps import get_route
from flask import Blueprint, request, jsonify

one_maps_routes = Blueprint('one_maps_routes', __name__)

# route that takes start and end coordinates and returns route 
# uses get_route(start, end)

@one_maps_routes.route('/get_cycling_route', methods=['GET'])
def get_cycling_route():
    data = request.get_json()
    start_address = data.get('start_address')
    end_address = data.get('end_address')
    result = get_route(start_address, end_address)

    return jsonify(result)