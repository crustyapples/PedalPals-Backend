from app.models import user as user_model, social_post as post_model, user_profile as profile_model, gamification as gamification_model, analytics as analytics_model, location as location_model, badge as badge_model, route as route_model
from bson import ObjectId
from flask import jsonify, request
import bcrypt
from app import mongo
from flask_jwt_extended import get_jwt_identity

class PostController:
    @staticmethod
    def get_posts(user_id):
        """
        Retrieves all posts from the Post collection in MongoDB and returns them in JSON format.
        
        :param user_id: (optional) The ObjectId of the user to filter posts by.
        :return: A Flask response object with a JSON payload containing all posts.
        """
        
        if user_id:
            print("Filtered by", user_id)
            posts_cursor = mongo.db.Post.find({"user_id": ObjectId(user_id)})

        else:
            posts_cursor = mongo.db.Post.find()

        posts_list  = [post for post in posts_cursor]

        # convert the _id, user fields to strings
        # inside each post, there is a comments array, where the comment[0] in the comments array should be converted to string

        for post in posts_list:
            post['_id'] = str(post['_id'])
            post['user'] = str(post['user'])
            post['user_id'] = str(post['user_id'])
            for comment in post['comments']:
                comment[0] = str(comment[0])

        print(posts_list)

        return posts_list

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

        if str(user['_id']) in post['likes']:
            # remove the like
            post['likes'].remove(str(user['_id']))
            mongo.db.Post.update_one({"_id": post['_id']}, {"$set": post})
            return jsonify({"message": "Post disliked!"}), 200
        else:
            post['likes'].append(str(user['_id']))
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
