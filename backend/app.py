from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Workout

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workouts.db"
db.init_app(app)


with app.app_context():
    db.create_all()
    print("✅ Tables created or already exist.")

@app.route("/generate-workout", methods=["GET", "POST"])
def generate_workout():
    from filters import prompt_filters, get_filtered_workout
    print("CONTENT-TYPE:", request.content_type)
    print("RAW BODY:", request.data)
    data = request.get_json()
    prompt = data.get("prompt")

    filters = prompt_filters(prompt)
    workouts = get_filtered_workout(filters)

    return jsonify([
        {
            "id": w.id,
            "name": w.name,
            "targeted_muscles": w.targeted_muscles,
            "difficulty": w.difficulty,
            "equipment": w.equipment,
            "sets": w.sets,
            "reps": w.reps
        }
        for w in workouts
    ])

@app.route("/add-workout", methods=["POST"])
def add_workout():
    data = request.get_json()
    new_workout = Workout(
        name=data["name"],
        type=data["type"],
        targeted_muscles = data["targeted_muscles"],
        difficulty=data["difficulty"],
        sets=data["sets"],
        reps=["reps"]
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(message="Workout added")

@app.route("/workouts", methods=["GET"])
def get_workout():
    workouts = Workout.query.all()
    return jsonify([
        {
            "id": w.id,
            "name": w.name,
            "type": w.type,
            "targeted_muscles": w.targeted_muscles,
            "difficulty": w.difficulty,
            "equipment": w.equipment,
            "sets": w.sets,
            "reps": w.reps
        }
        for w in workouts
    ])

if __name__ == "__main__":
    app.run(debug=True)