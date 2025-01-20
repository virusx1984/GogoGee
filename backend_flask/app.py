
import os
import sys
# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, project_root)
# print(f"Project root added to sys.path: {project_root}")
# print(f"Current sys.path: {sys.path}")

from flask import Flask, jsonify

from flask_cors import CORS
from backend_flask.models import db


"""Application factory pattern"""
app = Flask(__name__)

# Enable CORS
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://gogogee_test:111111@192.168.3.19:1521/orcl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
db.init_app(app)

# Import and register blueprints
from backend_flask.routes.auth_routes import auth_bp
from backend_flask.routes.user_routes import user_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask RESTful API!"})

if __name__ == '__main__':
    app.run(debug=True)
