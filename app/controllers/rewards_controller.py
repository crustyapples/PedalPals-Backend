from app import mongo
from flask import jsonify
from bson import ObjectId
import json
import requests

class RewardsController:
    @staticmethod
    def refresh_leaderboard():
        """
        Refreshes the leaderboard by retrieving user gamification data, sorting users based on their points,
        updating their leadership positions, and returning the updated leaderboard.
        
        Steps:
        1. Retrieve all user gamification data from the 'Gamification' collection in MongoDB.
        2. Sort the users in descending order based on their points.
        3. Update the 'leadership_position' field in MongoDB for each user based on their sorted position.
        4. Retrieve the updated user gamification data from MongoDB.
        5. Create a leaderboard list containing user names, points, and leadership positions.
        6. Return a Flask response with the leaderboard data in JSON format.
        
        :return: A Flask response object with a JSON payload containing the updated leaderboard.
        """
        # Get all the users from the Gamification collection
        user_gamification = mongo.db.Gamification.find()

        # Sort the users by points in descending order
        user_gamification = sorted(user_gamification, key=lambda x: x['points'], reverse=True)

        # Update the leadership_position for all users
        for index, user in enumerate(user_gamification):
            gamification = mongo.db.Gamification.find_one({"_id": user['_id']})
            gamification['leadership_position'] = index + 1
            mongo.db.Gamification.update_one({"_id": gamification['_id']}, {"$set": {"leadership_position": index + 1}})

        # Retrieve the updated user gamification data and prepare the leaderboard
        user_gamification = mongo.db.Gamification.find()
        user_gamification = sorted(user_gamification, key=lambda x: x['points'], reverse=True)
        leaderboard = [{'name': user['user'], 'points': user['points'], 'leadership_position': user['leadership_position']} for user in user_gamification]

        return jsonify({"message": leaderboard}), 200

