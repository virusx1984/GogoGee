from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models import db, Location
from ..schemas import LocationSchema
from .auth_routes import token_required
from datetime import datetime

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

location_bp = Blueprint('locations', __name__, url_prefix='/api/locations')

@location_bp.route('', methods=['GET'])
@token_required
def get_locations(current_user):
    try:
        locations = Location.query.all()
        return jsonify({
            'success': True,
            'data': locations_schema.dump(locations)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@location_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_location(current_user, id):
    try:
        location = Location.query.get(id)
        if not location:
            return jsonify({
                'success': False,
                'message': 'Location not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': location_schema.dump(location)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@location_bp.route('', methods=['POST'])
@token_required
def create_location(current_user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        # Validate and deserialize input
        try:
            location_data = location_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': err.messages
            }), 400

        # Create new location
        new_location = Location(
            **location_data,
            created_user_id=current_user.id,
            updated_user_id=current_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_location)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_location.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@location_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_location(current_user, id):
    try:
        location = Location.query.get(id)
        if not location:
            return jsonify({
                'success': False,
                'message': 'Location not found'
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        # Validate and update location fields
        try:
            update_data = location_schema.load(data, partial=True)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': err.messages
            }), 400

        for key, value in update_data.items():
            setattr(location, key, value)
            
        location.updated_user_id = current_user.id
        location.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': location.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@location_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_location(current_user, id):
    try:
        location = Location.query.get(id)
        if not location:
            return jsonify({
                'success': False,
                'message': 'Location not found'
            }), 404

        db.session.delete(location)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Location deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
