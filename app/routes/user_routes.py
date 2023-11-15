from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from app.controllers import user_controller, route_controller as route_controller, rewards_controller as rewards_controller, posts_controller as posts_controller
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, get_jwt_header
from flask import Blueprint, request, jsonify, redirect, url_for
from bson import ObjectId
import bcrypt
from app import mongo
from app.utils.find_nearby import find_nearby_coordinates
from app.utils.data_gov import get_nearest_pm25_and_weather
from app.gamification_strategies.bonus_strategy import BonusPointsStrategy
from app.gamification_strategies.standard_strategy import StandardPointsStrategy
from app.gamification_strategies.demo_strategy import DemoPointsStrategy
import json
import requests
import datetime
import math
import re

user_routes = Blueprint('user_routes', __name__)
strategy = DemoPointsStrategy()
user_control = user_controller.UserController()
route_control = route_controller.RouteController()
rewards_control = rewards_controller.RewardsController(strategy)

@user_routes.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.User.find_by_id(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    else:
        print("User",user.name)

    user_profile_id = user.user_profile
    
    # get user_profile object
    user_profile = profile_model.UserProfile.find_by_id(user_profile_id)

    gamification_id = user_profile.gamification
    analytics_id = user_profile.analytics

    # get the gamification and analytics objects
    gamification = gamification_model.Gamification.find_by_id(gamification_id)
    analytics = analytics_model.Analytics.find_by_id(analytics_id)

    user_posts = posts_controller.PostController.get_posts(user_id)
    
    friends_list = []
    for friend in user.friends_list:
        friends_list.append(str(friend))

    # from user object, get id, name, email, friend_list, location only
    user_dict = {
        "_id": user_id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "friends_list": friends_list,
        "location": user.location,
        "telegram": user_profile.telegram,
        "instagram": user_profile.instagram,
        "gamification": {
            "badgeCount": gamification.badgeCount,
            "badges": gamification.badges,
            "points": gamification.points,
            "leadership_position": gamification.leadership_position
        },
        "analytics": {
            "avg_speed": analytics.avg_speed,
            "total_distance": analytics.total_distance,
            "routes": analytics.routes
        },
        "posts": user_posts
    }

    return jsonify(user_dict)

@user_routes.route('/users', methods=['GET'])
# @jwt_required()
def get_users():
    users = mongo.db.User.find()
    
    user_list = []

    for user in users:
        userInfo = {
            "id": str(user['_id']),
            "username": user['username']
        }
        
        print(userInfo)
        user_list.append(userInfo)
        
    return jsonify(user_list)

@user_routes.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    name = data.get('name')
    password = data.get('password')

    return user_control.create_user(name, email, username, password, data)

@user_routes.route('/users/<user_id>', methods=['PUT'])
# @jwt_required()
def update_user(user_id):
    
    # current_user_email = get_jwt_identity()
    user = user_model.User.find_by_id(user_id)
    print(user.name)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    print(data)
    
    # from data, update the user object based on the fields that are present, write the code for this
    updated_fields = user.update_fields(data)
    user.update(user_id)

    # Return the updated fields
    return jsonify({"message": "User updated successfully"}), 200

@user_routes.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Convert the user_id string to an ObjectId
    user_obj_id = ObjectId(user_id)

    # Fetch the user document
    user = mongo.db.User.find_one({"_id": user_obj_id})
    profile_id = user['user_profile']
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Delete the user and related documents
    return user_control.delete_user(user_obj_id, profile_id)


@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    location = data.get('location')

    print(username)

    
    if len(username.strip()) == 0 or len(name.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
        return jsonify({'error': 'Please fill in all the text fields'})
    
    elif not re.match("^[a-zA-Z0-9]+$", username):
        return jsonify({'error': 'Username must contain only alphanumeric characters'})
    
    elif mongo.db.User.find_one({"username": username}):
        return jsonify({"error": "Please choose another username"})
    
    elif (not (1 <= len(username) <= 10)):
        print(len(username)) 
        return jsonify({"error": "Username should be between 1 and 10 characters"})
    
    elif not("@" in email):
        return jsonify({"error": "Email invalid"})
    
    elif mongo.db.User.find_one({"email": email}):
        return jsonify({"error": "Email already registered"})
    
    elif (not (8 <= len(password) <= 512)): 
        return jsonify({"error": "Invalid password. Your password should be between 8 and 512 characters"})

    elif (not re.match("^[a-zA-Z0-9]+$", password)): 
        return jsonify({"error": "Invalid password. Your password should contain alphanumeric characters only"})
    
    elif(password.lower() == username.lower()):
        return jsonify({"error": "Invalid password. Your password should not be the same as your username"})

    return user_control.create_user(name, email, username, password, location, data)


@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if len(email.strip()) == 0 or len(password.strip()) == 0:
        return jsonify({'error': 'Please fill in all the text fields'})
    
    elif not(mongo.db.User.find_one({"email": email})):
        return jsonify({'error': 'User not registered'})
    
    elif not("@" in email):
        return jsonify({'error': 'Email invalid'})

    # Fetch user from the database
    user = mongo.db.User.find_one({"email": email})
    print(user)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        access_token = create_access_token(identity=email)
        return jsonify({"access_token": access_token,"user_id": str(user['_id'])}), 200
    
    else:
        return jsonify({'error': 'Invalid password'})

    return jsonify({"message": "Invalid email or password",}), 401

@user_routes.route('/find-nearby-cyclists', methods=['POST'])
@jwt_required()
def find_nearby_cyclists():
    data = request.get_json()
    radius = data.get('radius')

    current_user_email = get_jwt_identity()
    current_user = mongo.db.User.find_one({"email": current_user_email})
    print(current_user['name'])

    if current_user["location"] is None:
        return jsonify({"message": "User has not shared location"}), 200

    current_user_location = tuple(map(float,current_user['location']['coordinates'].split(',')))

    # get all users except current user
    users = mongo.db.User.find({"email": {"$ne": current_user_email}})
    locations = []

    for user in users:
        # print(user)
        if user['location']:
            locations.append(tuple(map(float,user['location']['coordinates'].split(','))))

    nearby_locations, distances = find_nearby_coordinates(current_user_location,radius, locations)
            
    nearby_users = []
    for location in nearby_locations:
        
        # get all users for the location
        users = mongo.db.User.find({"location.coordinates": ','.join(map(str,location))})
        for user in users:
            distance = distances[nearby_locations.index(location)]
            # round distance to 2 decimal places
            distance = round(distance,2)

            userInfo = {
                "id": str(user['_id']),
                "username": user['username'],
                "distance": distance
            }

            if userInfo['id'] != str(current_user['_id']) and userInfo not in nearby_users:
                nearby_users.append(userInfo)
    
    print(nearby_users)

    return jsonify({"nearby_users": nearby_users}), 200


@user_routes.route('/add-friend/<friend_id>', methods=['POST'])
@jwt_required()
def add_friend(friend_id):
    current_user_email = get_jwt_identity()
    return user_control.add_friend(current_user_email, friend_id)

# route for removing friend
@user_routes.route('/remove-friend/<friend_id>', methods=['POST'])
@jwt_required()
def remove_friend(friend_id):
    current_user_email = get_jwt_identity()
    return user_control.remove_friend(current_user_email, friend_id)

@user_routes.route('/accept-route', methods=['POST'])
@jwt_required()
def accept_route():
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    route_geometry = data.get('route_geometry')
    route_instructions = data.get('route_instructions')
    route_name = data.get('route_name')
    route_summary = data.get('route_summary')
    route_start_coordinates = route_instructions[0][3]
    route_end_coordinates = route_instructions[-1][3]
    route_distance = route_summary['total_distance']
    route_time = route_summary['total_time']
    status = data.get('status')
    weather = data.get('weather')






    # Get the routes that user has done from their analytics object
    user_profile = mongo.db.User_Profile.find_one({"user_id": user['_id']})
    analytics = mongo.db.Analytics.find_one({"_id": user_profile['analytics']})
    gamification = mongo.db.Gamification.find_one({"_id": user_profile['gamification']})

    user_routes = analytics['routes']
    total_distance = float(analytics['total_distance'])
    avg_speed = float(analytics['avg_speed'])
    if avg_speed == 0:
        total_time = 0
    else:
        total_time = total_distance / avg_speed

    badge_count = gamification['badgeCount']
    badges = gamification['badges']
    points = int(gamification['points'])

    total_distance += route_distance
    
    total_time += route_time

    if total_time == 0:
        avg_speed = 0
    else:
        avg_speed = total_distance / total_time


    # if Route is Easy, add a bronze badge, if Medium, add a silver badge, if Hard, add a gold badge
    points_added = rewards_control.calculate_points(route_distance)
    points += points_added
    badge_added = rewards_control.calculate_badges(route_distance)
    badges.append(badge_added)
    badge_count += 1
    route_difficulty = rewards_control.calculate_difficulty(route_distance)

    print("Route Distance", route_distance)
    print("Time Taken", route_time)
    print("Points added:", points_added)
    print("Badge added:", badge_added)

    new_route = {
        "distance": route_distance,
        "time": route_time,
        "start_coordinates": route_start_coordinates,
        "end_coordinates": route_end_coordinates,
        "start_time": None,
        "end_time": None,
        "route_status": status,
        "traffic_info": None,
        "weather_status": weather,
        "route_difficulty": route_difficulty,
        "route_geometry": route_geometry,
        "date": datetime.datetime.now(),
        "route_summary": route_summary,
    }

    # Creating a new route object
    route = route_model.Route(**new_route)

    # Save the route object into the database
    route_id = route.save()

    print(route_id)

    # points += route_distance
    # if route_difficulty == "Easy":
    #     badge_count += 1
    #     points *= 1
    #     badges.append("bronze")
    # elif route_difficulty == "Medium":
    #     badge_count += 1
    #     points *= 2
    #     badges.append("silver")
    # else:
    #     badge_count += 1
    #     points *= 3
    #     badges.append("gold")

    user_routes.append(str(route_id))

    # call update_user() function to update the user's routes
    update_data = {
        "user_profile": {
            "analytics": {
                "avg_speed": avg_speed,
                "total_distance": total_distance,
                "routes": user_routes
            },
            "gamification": {
                "badgeCount": badge_count,
                "badges": badges,
                "points": points
            }
        }
    }

    user_id = str(user['_id'])
    update_data_json = json.dumps(update_data)

    # Replace with Base URL later
    requests.put(f'http://0.0.0.0:8039/users/{user_id}', data=update_data_json, headers={'Content-Type': 'application/json'})

    return jsonify({"route_id": str(route_id)}), 200


