from app import mongo
from flask import jsonify
from bson import ObjectId
import json
import requests
from app.utils.one_maps import get_route
from app.utils.data_gov import get_nearest_pm25_and_weather

class RouteController:
    @staticmethod
    def post_route(user, caption, route, timestamp):
        new_post = post_model.SocialPost(user=user['_id'], caption=caption, timestamp=timestamp, route=route)
        new_post.save()

        return jsonify({"message": "Route posted successfully!"}), 200
        
    @staticmethod
    def get_route(start,end):
        result = get_route(start,end)
        return jsonify(result)
        
    @staticmethod
    def get_weather_status(route_id):
        route = mongo.db.Route.find_one({"_id": ObjectId(route_id)})

        start_coordinates = route['start_coordinates']
        latitude, longitude = start_coordinates.split(',')
        
        pm25, weather = get_nearest_pm25_and_weather(latitude=float(latitude), longitude=float(longitude))

        weather = {
            "PM25": pm25,
            "weather": weather
        }

        return jsonify(weather)

    @staticmethod
    def refresh_leaderboard():
        # Logic for refreshing the leaderboard goes here
        # For demonstration, I'll just return a success message
        # In a real-world scenario, you would implement the logic to sort users based on points,
        # update their leaderboard positions, and return the updated leaderboard.

        return jsonify({"message": "Leaderboard refreshed successfully!"}), 200
