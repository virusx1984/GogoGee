import os
import sys
# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from flask import Flask
from backend_flask.models import User, db

app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://gogogee_test:111111@192.168.3.19:1521/orcl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_admin_user():
    with app.app_context():
        # Check if the admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("Admin user already exists.")
            return

        # Create the admin user
        admin_user = User(
            username='admin',
            name_eng='Admin User',
            name_chn='管理员',
            is_admin=True  # Set the user as an admin
        )
        admin_user.password = '111111'  # Hashes the password
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")

if __name__ == '__main__':
    create_admin_user()