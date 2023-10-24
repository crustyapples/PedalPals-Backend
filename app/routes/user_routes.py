from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import Blueprint, request, jsonify
from bson import ObjectId
import bcrypt
from app import mongo
from app.utils.find_nearby import find_nearby_coordinates

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
@jwt_required()
def update_user(user_id):
    
    current_user_email = get_jwt_identity()
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
    user = mongo.db.users.find_one({"email": current_user_email})
    caption = request.json.get('caption')
    route = request.json.get('route')

    new_post = post_model.SocialPost(user=user['_id'], caption=caption, route=route)
    # Insert new post into the "posts" collection
    mongo.db.posts.insert_one(new_post.__dict__)

    return jsonify({"message": "Post created successfully!"}), 201

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
    user = mongo.db.users.find_one({"email": current_user_email})
    friend = mongo.db.users.find_one({"_id": friend_id})

    if friend:
        # Update the user's friend list
        mongo.db.user_profile.update_one({"user_id": user['_id']}, {"$addToSet": {"friends": friend['name']}})
        return jsonify({"message": "Friend added successfully!"}), 200
    
    return jsonify({"message": "Friend not found!"}), 404
