from app import mongo
from flask import jsonify
from bson import ObjectId
import json
import requests
from app.utils.one_maps import get_route
from app.utils.data_gov import get_nearest_pm25_and_weather
from app.models import user as user_model, social_post as post_model, route as route_model, routepoints as route_point_model
from app.interfaces import route_planner_module as RoutePlanner

class RouteController:
    def __init__(self, planner: RoutePlanner):
        self.planner = planner
        pass

    def post_route(self,user, caption, route_id, timestamp):
        """
        Creates a new social post with the provided route information and saves it to the database.
        
        :param user: A dictionary representing the user posting the route. Must contain an '_id' field.
        :param caption: A string representing the caption of the post.
        :param route: A dictionary representing the route information.
        :param timestamp: A datetime object representing the time the post was created.
        :return: A Flask response object with a JSON payload indicating success.
        """

        # get route from Route collection using route which is the id
        route = route_model.Route.find_by_id(route_id)

        route_details = {
            "_id": route_id,
            "distance": route.distance,
            "time": route.time,
            "start_coordinates": route.start_coordinates,
            "end_coordinates": route.end_coordinates,
            "route_difficulty": route.route_difficulty,
            "route_geometry": route.route_geometry,
            "route_summary": route.route_summary,
        }

        new_post = post_model.SocialPost(user=user['username'], user_id=user['_id'],caption=caption, timestamp=timestamp, route=route_details)
        new_post.save()

        return jsonify({"message": "Route posted successfully!"}), 200
        
    def get_route(self,start, end):
        """
        Retrieves the optimal route between two points using the get_route function from the one_maps module.
        
        :param start: A string representing the starting coordinates of the route.
        :param end: A string representing the ending coordinates of the route.
        :return: A Flask response object with a JSON payload containing the route information.
        """
        result = self.planner.calculate_route(start, end)

        # get all the route points from the database
        try:
            route_points = route_point_model.RoutePoint.find_all()
            filtered_route_points = route_point_model.RoutePoint.filter_route_points(route_points, result['route_geometry'])
            result['route_points'] = filtered_route_points
        except:
            result['route_points'] = None

        return jsonify(result)
        
    def get_weather_status(self, route_id):
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

    def find_routes(self):
        """
        Retrieves all routes from the database.
        
        :return: A Flask response object with a JSON payload containing the routes.
        """
        routes = mongo.db.Route.find()
        route_list = []
        for route in routes:
            route['_id'] = str(route['_id'])
            route_list.append(route)

        return jsonify(route_list)
