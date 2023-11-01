from app import mongo
from flask import jsonify
from bson import ObjectId
import json
import requests

class RewardsController:

    @staticmethod
    def refresh_leaderboard():
        # Get all the users from the User collection
        user_gamification = mongo.db.Gamification.find()

        # Sort the users by points
        user_gamification = sorted(user_gamification, key=lambda x: x['points'], reverse=True)

        # Update the leadership_position for all users
        for index, user in enumerate(user_gamification):
            gamification = mongo.db.Gamification.find_one({"_id": user['_id']})
            gamification['leadership_position'] = index + 1
            mongo.db.Gamification.update_one({"_id": gamification['_id']}, {"$set": gamification})

        # Now return the actual leaderboard with the user names, their points and their leadership_position
        user_gamification = mongo.db.Gamification.find()
        user_gamification = sorted(user_gamification, key=lambda x: x['points'], reverse=True)
        leaderboard = []

        for user in user_gamification:
            leaderboard.append({
                "name": user['user'],
                "points": user['points'],
                "leadership_position": user['leadership_position']
            })

        return jsonify({"message": leaderboard}), 200
