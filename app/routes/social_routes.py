from flask import Blueprint, jsonify, request
from app import mongo
from app.models import social_post
from app.controllers import posts_controller
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, get_jwt_header

social_routes = Blueprint('social_routes', __name__)
post_control = posts_controller.PostController()

@social_routes.route('/posts', methods=['GET'])
def get_posts():
    return post_control.get_posts()

@social_routes.route('/like-post/<post_id>', methods=['POST'])
@jwt_required()
def like_post(post_id):
    return post_control.like_post(post_id)

@social_routes.route('/comment-post/<post_id>', methods=['POST'])
@jwt_required()
def comment_post(post_id):
    return post_control.comment_post(post_id)