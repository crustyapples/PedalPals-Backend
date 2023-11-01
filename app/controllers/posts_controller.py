from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from bson import ObjectId
from flask import jsonify
import bcrypt
from app import mongo

class PostController:
    @staticmethod
    def get_posts():
        posts = mongo.db.Post.find()
        return jsonify([post for post in posts])

    @staticmethod
    def create_post(self, post_data):
        # Create post object
        new_post = post_model.Post(**post_data)
        # Save post into the "Post" collection
        post_id = new_post.save()
        return jsonify({"message": "Post created successfully!", "post_id": str(post_id)}), 201

    @staticmethod
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

    @staticmethod
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