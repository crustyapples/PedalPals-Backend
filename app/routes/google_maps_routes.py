from app import mongo
from app.utils.google_maps import get_address_suggestions, get_location_coordinates
from flask import Blueprint, request, jsonify

google_maps_routes = Blueprint('google_maps_routes', __name__)

# route for address autocomplete
# 1. accept input address and return a list of possible addresses and their place ids
# uses get_address_suggestions(input_address) 
@google_maps_routes.route('/address-autocomplete', methods=['GET'])
def address_autocomplete():
    data = request.get_json()
    input_address = data.get('input_address')
    result = get_address_suggestions(input_address)
    print(result[0][1])

    return jsonify(result)

# route for reverse resolution of address to coordinates
# 1. accept address and return coordinates
# uses get_location_coordinates(place_id)
@google_maps_routes.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    data = request.get_json()
    place_id = data.get('place_id')
    result = get_location_coordinates(place_id)
    print(result)
    return jsonify(result)

