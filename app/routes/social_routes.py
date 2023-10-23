from flask import Blueprint, jsonify, request
from app import db
from app.models import social_post

social_routes = Blueprint('social_routes', __name__)

@social_routes.route('/posts', methods=['GET'])
def get_posts():
    posts = db.posts.find()
    return jsonify([post for post in posts])

# ... other CRUD operations ...