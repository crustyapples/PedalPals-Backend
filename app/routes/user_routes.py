from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, get_jwt_header
from flask import Blueprint, request, jsonify, redirect, url_for
from bson import ObjectId
import bcrypt
from app import mongo
from app.utils.find_nearby import find_nearby_coordinates
from app.utils.data_gov import get_nearest_pm25_and_weather
import json
import requests
import datetime

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
# @jwt_required()
def get_users():
    users_cursor = mongo.db.User.find()
    users_list = [user_model.User(**user).to_dict() for user in users_cursor]
    return jsonify(users_list)

@user_routes.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    name = data.get('name')
    password = data.get('password')

    # Check if user already exists
    existing_user = mongo.db.User.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Create user object
    new_user = user_model.User(name=name, email=email, username=username, password=None, user_profile=None, location=None)

    # Hash the password
    hashed_pw = new_user.set_password(password)

    # Save user into the "User" collection
    user_id = new_user.save()

    # Create user_profile object and save it
    new_profile = profile_model.UserProfile(name=name, user_id=user_id, email=email, telegram=data.get('Telegram', ''), instagram=data.get('Instagram', ''), pals=data.get('Pals', 0), points=data.get('Points', 0), friends=[], analytics=None, gamification=None)
    profile_id = new_profile.save()

    # Create analytics object and save it
    new_analytics = analytics_model.Analytics(user=name, user_id=user_id, avg_speed=0, total_distance=0, routes=[])
    analytics_id = new_analytics.save()

    # Create gamification object and save it
    new_gamification = gamification_model.Gamification(user=name, badgeCount=0, leadership_position=0, badges=[])
    gamification_id = new_gamification.save()

    # Update user_profile with analytics and gamification references
    new_profile.analytics = analytics_id
    new_profile.gamification = gamification_id
    new_profile.update(profile_id)

    # Update user with user_profile
    new_user.user_profile = profile_id
    new_user.update(user_id)

    return jsonify({"message": "User added successfully!", "user_id": str(user_id)}), 201

@user_routes.route('/users/<user_id>', methods=['PUT'])
# @jwt_required()
def update_user(user_id):
    
    # current_user_email = get_jwt_identity()
    user = user_model.User.find_by_id(user_id)
    print(user.name)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    
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

    # Fetch the user's profile document
    profile = mongo.db.User_Profile.find_one({"_id": profile_id})
    print(profile)
    # Delete the related analytics and gamification documents
    if profile:
        print("Found Profile")
        if 'analytics' in profile:
            print("Found Analytics")
            print("Deleting Analytics")
            mongo.db.Analytics.delete_one({"_id": profile['analytics']})
        if 'gamification' in profile:
            print("Found Gamification")
            print("Deleting Gamification")
            mongo.db.Gamification.delete_one({"_id": profile['gamification']})
        # Delete the user's profile document
        print("Deleting Profile")
        mongo.db.User_Profile.delete_one({"_id": profile['_id']})
    
    # Finally, delete the user document
    print("Deleting User")
    mongo.db.User.delete_one({"_id": user_obj_id})

    return jsonify({"message": "User deleted successfully"}), 200


@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    location = data.get('location')

    # Check if user already exists
    existing_user = mongo.db.User.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Create and save the user
    new_user = user_model.User(name=name, email=email, username=username, password=None, user_profile=None, location=location)
    hashed_pw = new_user.set_password(password)
    user_id = new_user.save()

    # Create user_profile object and save it
    new_profile = profile_model.UserProfile(name=name, user_id=user_id, email=email, telegram=data.get('Telegram', ''), instagram=data.get('Instagram', ''), pals=data.get('Pals', 0), points=data.get('Points', 0), friends=[], analytics=None, gamification=None)
    profile_id = new_profile.save()

    # Create analytics object and save it
    new_analytics = analytics_model.Analytics(user=name, user_id=user_id, avg_speed=0, total_distance=0, routes=[])
    analytics_id = new_analytics.save()

    # Create gamification object and save it
    new_gamification = gamification_model.Gamification(user=name, badgeCount=0, leadership_position=0, badges=[])
    gamification_id = new_gamification.save()

    # Update user profile with analytics and gamification references
    new_profile.analytics = analytics_id
    new_profile.gamification = gamification_id
    new_profile.update(profile_id)

    # Update user with user_profile
    new_user.user_profile = profile_id
    new_user.update(user_id)

    return jsonify({"message": "User created successfully","user_id": str(user_id)}), 201


@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Fetch user from the database
    user = mongo.db.User.find_one({"email": email})
    print(user)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        access_token = create_access_token(identity=email)
        return jsonify({"access_token": access_token,"user_id": str(user['_id'])}), 200

    return jsonify({"message": "Invalid email or password",}), 401

@user_routes.route('/post-cycle-route', methods=['POST'])
@jwt_required()
def post_cycle_route():
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    
    caption = request.json.get('caption')
    route = request.json.get('route')

    timestamp = datetime.datetime.now()

    new_post = post_model.SocialPost(user=user['_id'], caption=caption, timestamp=timestamp, route=route)
    new_post.save()
    
    return jsonify({"message": "Post created successfully!"}), 201

# Routes for liking and commenting 

@user_routes.route('/like-post/<post_id>', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    post = mongo.db.Post.find_one({"_id": ObjectId(post_id)})

    if not post:
        return jsonify({"message": "Post not found!"}), 404

    # update likes
    post['likes'] += 1
    mongo.db.Post.update_one({"_id": post['_id']}, {"$set": post})

    return jsonify({"message": "Post liked successfully!"}), 200

@user_routes.route('/comment-post/<post_id>', methods=['POST'])
@jwt_required()
def comment_post(post_id):
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    post = mongo.db.Post.find_one({"_id": ObjectId(post_id)})

    if not post:
        return jsonify({"message": "Post not found!"}), 404

    # update comments, should be a tuple that contains user and comment
    comment = request.json.get('comment')
    comment = (user['_id'], comment)

    post['comments'].append(comment)
    mongo.db.Post.update_one({"_id": post['_id']}, {"$set": post})

    return jsonify({"message": "Commented on post successfully!"}), 200

@user_routes.route('/find-nearby-cyclists', methods=['GET'])
@jwt_required()
def find_nearby_cyclists():
    data = request.get_json()
    radius = data.get('radius')

    current_user_email = get_jwt_identity()
    current_user = mongo.db.User.find_one({"email": current_user_email})
    print(current_user['name'])

    current_user_location = tuple(map(float,current_user['location']['coordinates'].split(',')))
    users = mongo.db.User.find({"location.coordinates": {"$ne": current_user['location']['coordinates']}})
    locations = []

    for user in users:
        print(user)
        locations.append(tuple(map(float,user['location']['coordinates'].split(','))))

    nearby_locations = find_nearby_coordinates(current_user_location,radius, locations)

    nearby_users = []
    for location in nearby_locations:
        print(','.join(map(str,location)))
        user = mongo.db.User.find_one({"location.coordinates": ','.join(map(str,location))})
        print(user)
        nearby_users.append(user['email'])

    return jsonify({"nearby_users": nearby_users}), 200


@user_routes.route('/add-friend/<friend_id>', methods=['POST'])
@jwt_required()
def add_friend(friend_id):
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    friend = mongo.db.User.find_one({"_id": ObjectId(friend_id)})

    if not friend:
        return jsonify({"message": "Friend not found!"}), 404

    # update friend_list with the new friend
    user['friends_list'].append(friend['_id'])
    mongo.db.User.update_one({"_id": user['_id']}, {"$set": user})

    return jsonify({"message": "Friend added successfully!"}), 200

# route for removing friend
@user_routes.route('/remove-friend/<friend_id>', methods=['POST'])
@jwt_required()
def remove_friend(friend_id):
    current_user_email = get_jwt_identity()
    user = mongo.db.User.find_one({"email": current_user_email})
    friend = mongo.db.User.find_one({"_id": ObjectId(friend_id)})

    if not friend:
        return jsonify({"message": "Friend not found!"}), 404

    # update friend_list with the new friend
    user['friends_list'].remove(friend['_id'])
    mongo.db.User.update_one({"_id": user['_id']}, {"$set": user})

    return jsonify({"message": "Friend removed successfully!"}), 200

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

    # route difficulty is based on distance, either Easy, Medium, Hard
    if route_distance < 10000:
        route_difficulty = "Easy"
    elif route_distance < 20000:
        route_difficulty = "Medium"
    else:
        route_difficulty = "Hard"

    latitude, longitude = route_start_coordinates.split(',')
    pm25, weather = get_nearest_pm25_and_weather(latitude=float(latitude), longitude=float(longitude))

    weather = {
        "PM25": pm25,
        "weather": weather
    }

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
        "route_geometry": route_geometry
    }

    # Creating a new route object
    route = route_model.Route(**new_route)

    # Save the route object into the database
    route_id = route.save()

    print(route_id)

    # Get the routes that user has done from their analytics object
    user_profile = mongo.db.User_Profile.find_one({"user_id": user['_id']})
    analytics = mongo.db.Analytics.find_one({"_id": user_profile['analytics']})
    gamification = mongo.db.Gamification.find_one({"_id": user_profile['gamification']})

    user_routes = analytics['routes']
    total_distance = float(analytics['total_distance'])
    avg_speed = float(analytics['avg_speed'])
    total_time = total_distance / avg_speed

    badge_count = gamification['badgeCount']
    badges = gamification['badges']
    points = int(gamification['points'])

    total_distance += route_distance
    points += route_distance
    total_time += route_time
    avg_speed = total_distance / total_time

    # if Route is Easy, add a bronze badge, if Medium, add a silver badge, if Hard, add a gold badge
    if route_difficulty == "Easy":
        badge_count += 1
        points *= 1
        badges.append("bronze")
    elif route_difficulty == "Medium":
        badge_count += 1
        points *= 2
        badges.append("silver")
    else:
        badge_count += 1
        points *= 3
        badges.append("gold")

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
    requests.put(f'http://127.0.0.1:8000/users/{user_id}', data=update_data_json, headers={'Content-Type': 'application/json'})

    return jsonify({"message": "Route accepted successfully!"}), 200