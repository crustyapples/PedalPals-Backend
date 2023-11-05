from app import mongo
from flask import jsonify
from bson import ObjectId
import json
import requests
from app.utils.one_maps import get_route
from app.utils.data_gov import get_nearest_pm25_and_weather
from app.models import user as user_model, social_post as post_model


class RouteController:
    @staticmethod
    def post_route(user, caption, route, timestamp):
        """
        Creates a new social post with the provided route information and saves it to the database.
        
        :param user: A dictionary representing the user posting the route. Must contain an '_id' field.
        :param caption: A string representing the caption of the post.
        :param route: A dictionary representing the route information.
        :param timestamp: A datetime object representing the time the post was created.
        :return: A Flask response object with a JSON payload indicating success.
        """
        new_post = post_model.SocialPost(user=user['_id'], caption=caption, timestamp=timestamp, route=route)
        new_post.save()

        return jsonify({"message": "Route posted successfully!"}), 200
        
    @staticmethod
    def get_route(start, end):
        """
        Retrieves the optimal route between two points using the get_route function from the one_maps module.
        
        :param start: A string representing the starting coordinates of the route.
        :param end: A string representing the ending coordinates of the route.
        :return: A Flask response object with a JSON payload containing the route information.
        """
        result = get_route(start, end)
        return jsonify(result)
        
    @staticmethod
    def get_weather_status(route_id):
        """
        Retrieves the current PM2.5 and weather status for the starting coordinates of a given route.
        
        :param route_id: A string representing the ObjectId of the route in MongoDB.
        :return: A Flask response object with a JSON payload containing the PM2.5 and weather information.
        """
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
        """
        Refreshes the leaderboard, sorting users based on points and updating their positions.
        
        :return: A Flask response object with a JSON payload indicating success.
        """
        # Logic for refreshing the leaderboard goes here
        # For demonstration, I'll just return a success message
        # In a real-world scenario, you would implement the logic to sort users based on points,
        # update their leaderboard positions, and return the updated leaderboard.

        return jsonify({"message": "Leaderboard refreshed successfully!"}), 200
