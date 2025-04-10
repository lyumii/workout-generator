from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = "workout"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    targeted_muscles = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.String(20), nullable=True)
    equipment = db.Column(db.String(100))
    source = db.Column(db.String(20), default="AI")
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class WorkoutHistory(db.Model):
    __tablename__ = "savedworkouts"
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String, nullable=False)
    workout_data = db.Column(MutableList.as_mutable(JSON), nullable=False) 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "workouts": self.workout_data,
            "timestamp": self.timestamp.isoformat()
        }