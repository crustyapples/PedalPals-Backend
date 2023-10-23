from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models import social_post as post_model
from app.models import user
from app import mongo

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()  # Fetch all users from the "users" collection
    return jsonify([user for user in users])

@user_routes.route('/users', methods=['POST'])
def add_user():
    # Get user details from request data
    data = request.json
    new_user = user.User(
        data['user_id'],
        data['email'],
        data['password'],
        data['analytics'],
        data['gamification'],
        data.get('friends_list', [])
    )
    db.users.insert_one(new_user.__dict__)  # Insert the user into the "users" collection
    return jsonify({"message": "User added successfully!"}), 201

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check if user already exists
    existing_user = mongo.db.users.find_one({"email": email})
    existing_user = mongo.users.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    user = User(email=email)
    user.set_password(password)
    db.users.insert_one(user)

    return jsonify({"message": "User created successfully"}), 201

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = mongo.db.users.find_one({"email": email})
    if not user or not User.check_password(user, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user['email'])
    return jsonify({"access_token": access_token}), 200

@user_routes.route('/post-cycle-route', methods=['POST'])
def post_cycle_route():
    user = ...  # Get logged-in user
    caption = request.form.get('caption')
    route = request.form.get('route')
    new_post = post_model.SocialPost(user=user, caption=caption, route=route)
    # Save new_post to storage
    return jsonify({"message": "Post created successfully!"}), 201

@user_routes.route('/find-nearby-cyclists', methods=['GET'])
def find_nearby_cyclists():
    user_location = request.args.get('location')  # Example: "lat,long"
    nearby_users = user_model.User.get_nearby_users(user_location)
    return jsonify(nearby_users)

@user_routes.route('/add-friend/<friend_id>', methods=['POST'])
def add_friend(friend_id):
    user = ...  # Get logged-in user
    friend = ...  # Retrieve the user with friend_id from storage
    if friend:
        user.add_friend(friend)
        return jsonify({"message": "Friend added successfully!"}), 200
    return jsonify({"message": "Friend not found!"}), 404