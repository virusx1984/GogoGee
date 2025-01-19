from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configuration
SECRET_KEY = 'your-secret-key-here'  # TODO: Move to config
TOKEN_EXPIRATION = 3600  # 1 hour

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({
                'success': False,
                'message': 'Token is invalid'
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400

        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION)
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
