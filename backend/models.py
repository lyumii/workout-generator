from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = "workout"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    targeted_muscles = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    sets = db.Column(db.Integer)
    reps = db.Column(db.String(20))
    equipment = db.Column(db.String(100))
    source = db.Column(db.String(20), default="AI")
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)