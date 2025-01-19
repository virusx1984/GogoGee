from flask import Blueprint, request, jsonify
from models import User, db
from schemas import UserSchema

user_bp = Blueprint('user', __name__)

# Initialize Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200

# Add a new user
@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  # In production, hash the password before saving
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

# Delete a user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200