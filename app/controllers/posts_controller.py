from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from bson import ObjectId
from flask import jsonify, request
import bcrypt
from app import mongo
from flask_jwt_extended import get_jwt_identity

class PostController:
    @staticmethod
    def get_posts():
        """
        Retrieves all posts from the Post collection in MongoDB and returns them in JSON format.
        
        :return: A Flask response object with a JSON payload containing all posts.
        """
        posts = mongo.db.Post.find()
        return jsonify([post for post in posts])

    @staticmethod
    def create_post(post_data):
        """
        Creates a new post in the Post collection in MongoDB with the provided post data.
        
        :param post_data: A dictionary containing the data for the new post.
        :return: A Flask response object with a JSON payload indicating success and the ID of the created post.
        """
        new_post = post_model.Post(**post_data)
        post_id = new_post.save()
        return jsonify({"message": "Post created successfully!", "post_id": str(post_id)}), 201

    @staticmethod
    def like_post(post_id):
        """
        Increases the like count of a specific post by one. 
        
        :param post_id: The ObjectId of the post in MongoDB.
        :return: A Flask response object with a JSON payload indicating success or an error message if the post is not found.
        """
        current_user_email = get_jwt_identity()
        user = mongo.db.User.find_one({"email": current_user_email})
        post = mongo.db.Post.find_one({"_id": ObjectId(post_id)})

        if not post:
            return jsonify({"message": "Post not found!"}), 404

        post['likes'] += 1
        mongo.db.Post.update_one({"_id": post['_id']}, {"$set": post})

        return jsonify({"message": "Post liked successfully!"}), 200

    @staticmethod
    def comment_post(post_id):
        """
        Adds a comment to a specific post. The comment is associated with the current user.
        
        :param post_id: The ObjectId of the post in MongoDB.
        :return: A Flask response object with a JSON payload indicating success or an error message if the post is not found.
        """
        current_user_email = get_jwt_identity()
        user = mongo.db.User.find_one({"email": current_user_email})
        post = mongo.db.Post.find_one({"_id": ObjectId(post_id)})

        if not post:
            return jsonify({"message": "Post not found!"}), 404

        comment = request.json.get('comment')
        comment_tuple = (str(user['_id']), comment)

        post['comments'].append(comment_tuple)
        mongo.db.Post.update_one({"_id": post['_id']}, {"$set": post})

        return jsonify({"message": "Commented on post successfully!"}), 200