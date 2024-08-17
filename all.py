# Question 1 Task:1 Setting Up the Flask Environment and Database Connection
# app.py
from flask import flask
from flask_marshmallow import Marshmallow
import mysql.connector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Marshmallow
ma = Marshmallow(app)
# Establish MYSQL connection
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = db.cursor()
#Create tables if they do not exsit 
cursor.execute("""
CREATE TABLE IF NOT EXISTS Members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS WorkoutSessions (
    id INTO AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    session_date DATE,
    duration INT,
    FOREIGN KEY (member_id) REFERENCES Memebers(id)
)
""")

db.commit()
@app.route('/')
def index():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)

# Question 1 Task:2 Implementing CRUD Operations for Members
from falsk import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

db.create_all()
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or not 'name' in data or not 'email' in data:
        return jsonify({'error': 'Bad Request', 'message': 'Name and email are required'}), 400
    
    new_member = Member(name=data['name'], email=data['email'])
    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member added sucessfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'Message': str(e)}), 500
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'error': 'Not Found', 'message': 'Member not found'}), 404
    return jsonify({'id': member.id, 'name': member.name, 'email': member.email}), 200
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Bad Request', 'message': 'Request body is missing'}), 400
    member = Member.query.get(id)
    if not member:
        return jsonify({'error': 'Not Found', 'message': 'Member not found'}), 404
    
    if 'name' in data:
        member.name = data['name']
        if 'eamil' in data:
            member.email = data['email']
        try:
            db.session.commit()
            return jsonify({'message': 'Member updated sucessfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'error': 'Not Found', 'message': 'Member not found'}), 404
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted sucessfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Question 1 Task:3 Managing Workout Sessions 
# 1. Schedule a Workout Session
# Endpoint: POST/workouts
# Description: This endpoint allows you to schedule a new workout session.

# Request Body:
{"memberID": "string",
 "date": "YYYY-MM-DD",
 "time": "HH:MM",
 "duration": "integer", // in minutes
 "type": "string",      // e.g., "Cardio", "Strength Training"
 "notes": "string"      // optional

}
#Response:

{
  "message": "Workout session scheduled successfully",
  "workoutId": "string"
}

# 2 Update a Workout Session
# End point: PUT/workouts/{workoutID}
#Description: This endpoint allows you to update an existing workout session.

#Request Body:
{"date": "YYYY-MM-DD",
 "time": "HH:MM",
 "duration": "integer", // in minutes
 "type": "string",      // e.g., "Cardio", "Strength Training"
 "notes": "string"      // optional
}
#Response:

{
  "message": "Workout session updated successfully"
}
# 3 View a Workout Session
#EndPoint: GET/workout/{workoutID}
#Description: This endpoint allows you to view the details of a specific workout session.

#Response:
{
  "workoutId": "string",
  "memberId": "string",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "duration": "integer",  // in minutes
  "type": "string",       // e.g., "Cardio", "Strength Training"
  "notes": "string"       // optional
}

# 4 Retrieve all Workout Sessions for a specific Memeber
#Description: This endpoint allows you to retrieve all workout sessions for a specific member.

#Response:

[
  {
    "workoutId": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "duration": "integer",  // in minutes
    "type": "string",       // e.g., "Cardio", "Strength Training"
    "notes": "string"       // optional
  },
  {
    "workoutId": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "duration": "integer",  // in minutes
    "type": "string",       // e.g., "Cardio", "Strength Training"
    "notes": "string"       // optional
  }
  // More workout sessions
]

# 5 Delete a Workout Session

#Endpoint: DELETE /workouts/{workoutId}

#Description: This endpoint allows you to delete a specific workout session.

#Response:

{
  "message": "Workout session deleted successfully"
}

