from flask import Blueprint, request, jsonify
from backend_flask.models import User
from backend_flask.schemas import UserSchema
from backend_flask import db

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

# Initialize Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': users_schema.dump(users)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@user_bp.route('/', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        # Validate input data
        errors = user_schema.validate(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation errors',
                'errors': errors
            }), 400

        new_user = User(
            username=data['username'],
            password=data['password']  # TODO: Hash password before saving
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user_schema.dump(new_user)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
