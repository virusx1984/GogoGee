from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..routes.auth_routes import token_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/', methods=['GET'])
@cross_origin()
@token_required
def get_dashboard_data(current_user):
    # Read the dashboard.html file
    with open('ui/web_ui/dashboard.html', 'r') as file:
        dashboard_content = file.read()
    
    return jsonify({
        'success': True,
        'content': dashboard_content,
        'scripts': [
            'https://cdn.jsdelivr.net/npm/chart.js',
            'js/dashboard.js'
        ],
        'styles': [
            'css/dashboard.css'
        ]
    }) 