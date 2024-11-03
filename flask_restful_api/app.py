from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from models import db, Task
from schemas import TaskSchema

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'user' and data['password'] == 'password':
        session['logged_in'] = True
        session['username'] = data['username']
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'})

@app.route('/protected', methods = ['POST'])
def protected():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({'message': f'Welcome, {session["username"]}!'})
    return redirect(url_for('login')) # Redirect to login if not logged in

@app.route('/logout', methods = ['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = task_schema.load(request.get_json())
        new_task = Task(**task_data)
        db.session.add(new_task)
        db.session.commit()
        return jsonify(task_schema.dump(new_task)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400  # Bad Request

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task_schema.dump(task))
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        try:
            task_data = task_schema.load(request.get_json(), partial=True)
            task.description = task_data.get('description', task.description)
            task.completed = task_data.get('completed', task.completed)
            db.session.commit()
            return jsonify(task_schema.dump(task))
        except ValidationError as err:
            return jsonify(err.messages), 400
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'}), 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)