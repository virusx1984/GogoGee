from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import db

# Import the user_routes Blueprint
from routes.user_routes import user_bp

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://gogogee_test:111111@192.168.3.19:1521/orcl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # Initialize SQLAlchemy with the Flask app instance

app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)