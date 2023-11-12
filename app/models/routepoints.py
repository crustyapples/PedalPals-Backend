from flask_bcrypt import Bcrypt
from bson import ObjectId
from app import mongo 
import polyline
from geopy.distance import distance
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import numpy as np
from math import cos, radians


class RoutePoint:
    def __init__(self, name, pointType, coordinates, description=None, details=None, postal_code=None):
        self.name = name
        self.type = pointType
        self.coordinates = coordinates
        self.description = description
        self.details = details
        self.postal_code = postal_code

    def save(self):
        route_point_collection = mongo.db.RoutePoints
        self.id = route_point_collection.insert_one(self.__dict__).inserted_id
        return self.id

    @staticmethod
    def find_all():
        route_point_collection = mongo.db.RoutePoints
        return route_point_collection.find()

    @staticmethod
    def is_close_to_route(point, route_line, max_distance_meters=2000):
        """Check if the point is close to the route using Shapely."""

        # Convert point coordinates from string to tuple of floats
        if isinstance(point['coordinates'], str) and point['coordinates'] != '(N/A, N/A)':
            point_coords = point['coordinates'].strip('()')
            lat, lon = map(float, point_coords.split(', '))
            point_coords = (lat, lon)
            point_geom = Point(point_coords)

            # Calculate distance in degrees
            distance_in_degrees = point_geom.distance(route_line)

            # Convert distance from degrees to meters
            # Assuming an average length of a degree of latitude in meters
            meters_per_degree = 111320 * cos(radians(lat))
            distance_in_meters = distance_in_degrees * meters_per_degree

            return distance_in_meters <= max_distance_meters

        
        return False

    @staticmethod
    def filter_route_points(route_points, route_geometry):
        """Filter and return route points that are close to the simplified route."""
        # Decode and simplify the route geometry
        route_coords = polyline.decode(route_geometry)
        route_line = LineString(route_coords)  # Simplify tolerance in degrees

        # Filter route points that are close to the route
        filtered_route_points = []
        for rp in route_points:
            if RoutePoint.is_close_to_route(rp, route_line):
                rp['_id'] = str(rp['_id'])
                filtered_route_points.append(rp)

        return filtered_route_points
        