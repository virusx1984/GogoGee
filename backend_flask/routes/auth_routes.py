from flask import Blueprint, request, jsonify
from ..models import User
from ..models import db
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_cors import cross_origin
import pdb

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configuration
SECRET_KEY = 'your-secret-key-here'  # TODO: Move to config
TOKEN_EXPIRATION = 3600  # 1 hour

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401

        try:
            # Remove 'Bearer ' prefix if present
            token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise Exception('User not found')
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Token is invalid'
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
             supports_credentials=True,
             allow_headers=["Content-Type", "Authorization"])
def login():
    if request.method == 'OPTIONS':
        # Preflight request. Reply successfully:
        response = jsonify({'success': True})
        return response
    
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400

        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.verify_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRATION)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'success': True,
            'token': token,
            'expires_in': TOKEN_EXPIRATION
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@auth_bp.route('/validate', methods=['GET'])
@token_required
def validate_token(current_user):
    return jsonify({
        'success': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username
        }
    }), 200

@auth_bp.route('/user', methods=['GET'])
@cross_origin(origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
             supports_credentials=True,
             allow_headers=["Content-Type", "Authorization"])
@token_required
def get_user(current_user):
    return jsonify({
        'success': True,
        'name_eng': current_user.name_eng,
        'username': current_user.username,
        'id': current_user.id
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@cross_origin(origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
             supports_credentials=True,
             allow_headers=["Content-Type", "Authorization"])
@token_required
def logout(current_user):
    # In a more complex system, you might want to invalidate the token
    return jsonify({
        'success': True,
        'message': 'Successfully logged out'
    }), 200
