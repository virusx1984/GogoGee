from flask import Flask, jsonify
from flask_cors import CORS
from backend_flask import db, create_app

app = create_app()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask RESTful API!"})

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
