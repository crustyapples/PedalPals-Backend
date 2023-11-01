from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from bson import ObjectId
from flask import jsonify
import bcrypt
from app import mongo

class UserController:
    @staticmethod
    def create_user(name, email, username, password, location, data):
        # Check if user already exists
        existing_user = mongo.db.User.find_one({"email": email})
        if existing_user:
            return jsonify({"message": "Email already registered"}), 400

        # Create user object
        new_user = user_model.User(name=name, email=email, username=username, password=None, user_profile=None, location=location)

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

        return jsonify({"message": "User created successfully!", "user_id": str(user_id)}), 201

    @staticmethod
    def delete_user(user_obj_id, profile_id):
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

    @staticmethod
    def update_user(user_id, fields):
        user = User.find_by_id(user_id)
        if user:
            user.update_fields(fields)
            user.update(user_id)
            return True
        return False

    @staticmethod
    def check_user_password(user_id, password):
        user = User.find_by_id(user_id)
        if user and user.check_password(password):
            return True
        return False

    @staticmethod
    def get_user_by_email(email):
        return User.find_by_email(email)

    @staticmethod
    def get_user_by_id(user_id):
        return User.find_by_id(user_id)
