from app.controllers import rewards_controller as rewards_controller
from flask import Blueprint, request, jsonify
from bson import ObjectId
import bcrypt
from app import mongo
from app.gamification_strategies.bonus_strategy import BonusPointsStrategy
from app.gamification_strategies.standard_strategy import StandardPointsStrategy

strategy = BonusPointsStrategy()
rewards_control = rewards_controller.RewardsController(strategy=strategy)

gamification_routes = Blueprint('gamification_routes', __name__)
@gamification_routes.route('/refresh-leaderboard', methods=['POST'])
def refresh_leaderboard():
    return rewards_control.refresh_leaderboard()