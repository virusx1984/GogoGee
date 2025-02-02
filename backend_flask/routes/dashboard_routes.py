from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..models import User
from .auth_routes import token_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('', methods=['GET'])
@cross_origin(
    origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"]
)
@token_required
def get_dashboard_data(current_user):
    try:
        # Your dashboard data logic here
        return jsonify({
            'success': True,
            'data': {
                'stats': [
                    {'label': 'Total Users', 'value': '150'},
                    {'label': 'Active Projects', 'value': '12'},
                    {'label': 'Completed Tasks', 'value': '45'}
                ],
                'activities': [
                    {
                        'date': '2024-02-02',
                        'activity': 'Project Update',
                        'user': 'John Doe',
                        'status': 'Completed'
                    },
                    # ... more activities
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 