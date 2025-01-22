from flask import Blueprint, request, jsonify
from ..models import User
from ..schemas import UserSchema
from ..models import db

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

# Initialize Marshmallow schemas with session
from ..models import db
user_schema = UserSchema(session=db.session)
users_schema = UserSchema(many=True, session=db.session)

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
            password=data['password'],  # Will be hashed by User model
            name_eng=data.get('name_eng', ''),
            name_chn=data.get('name_chn', ''),
            is_active=data.get('is_active', True),
            is_admin=data.get('is_admin', False),
            created_user_id=None,  # TODO: Set to current user ID
            updated_user_id=None   # TODO: Set to current user ID
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
