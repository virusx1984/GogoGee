from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    description2 = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    fullname = db.Column(db.String(120)) # Added fullname column
    othername = db.Column(db.String(120))

    def __repr__(self):
        return f'<Task {self.description}>'
    
