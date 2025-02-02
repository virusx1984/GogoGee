import os
import sys
# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, project_root)
# print(f"Project root added to sys.path: {project_root}")
# print(f"Current sys.path: {sys.path}")

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend_flask.models import db


"""Application factory pattern"""
def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Configure CORS
    CORS(app, 
        resources={
            r"/api/*": {
                "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Content-Type", "Authorization"],
                "max_age": 3600
            }
        },
        supports_credentials=True
    )

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://gogogee_test:111111@192.168.3.19:1521/orcl'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from backend_flask.routes.auth_routes import auth_bp
    from backend_flask.routes.user_routes import user_bp
    from backend_flask.routes.menu_routes import menu_bp
    from backend_flask.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(menu_bp)
    app.register_blueprint(dashboard_bp)

    # Add this route for debugging
    @app.before_request
    def before_request():
        print('Request Headers:', request.headers)
        print('Request Method:', request.method)
        print('Request URL:', request.url)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Flask RESTful API!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
