from app.controllers import rewards_controller as rewards_controller
from flask import Blueprint, request, jsonify
from bson import ObjectId
import bcrypt
from app import mongo

rewards_control = rewards_controller.RewardsController()

gamification_routes = Blueprint('gamification_routes', __name__)
@gamification_routes.route('/refresh-leaderboard', methods=['POST'])
def refresh_leaderboard():
    return rewards_control.refresh_leaderboard()