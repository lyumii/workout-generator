from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Workout, WorkoutHistory
from sqlalchemy.orm.attributes import flag_modified


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workouts.db"
db.init_app(app)


with app.app_context():
    db.create_all()
    print("✅ Tables created or already exist.")
    
@app.route("/generate-workout", methods=["GET", "POST"])
def generate_workout():
    if request.method == "GET":
        return jsonify({"message": "This route accepts POST requests with a prompt."})

    from filters_engine import prompt_filters, get_filtered_workout
    
    print("CONTENT-TYPE:", request.content_type)
    print("RAW BODY:", request.data)
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]
    filters = prompt_filters(prompt)
    workouts = get_filtered_workout(filters, prompt)

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

@app.route("/browse/<int:id>", methods=["PUT"])
def edit_workout(id):
    workout = WorkoutHistory.query.get_or_404(id)
    data = request.get_json()

    index = data.get("index")
    new_sets = data.get("sets")
    new_reps = data.get("reps")

    try:
        if new_sets is not None:
            workout.workout_data[index]["sets"] = new_sets
        if new_reps is not None:
            workout.workout_data[index]["reps"] = new_reps

        print(f"Updating workout {id}, index {index}, sets: {new_sets}, reps: {new_reps}")
        flag_modified(workout, "workout_data")

        db.session.commit()
        return jsonify({"message": "Updated!!", "workout": workout.to_dict()}), 201
    
    except (IndexError, TypeError):
        return jsonify({"error": "Invalid index or workout structure"}), 400
    

@app.route("/browse/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    workout = WorkoutHistory.query.get_or_404(id)
    data = request.get_json()
    index = data.get("index")

    try: 
        del workout.workout_data[index]
        db.session.commit()
        return jsonify({"message": "Removed!", "workout": workout.to_dict()}), 201
    
    except (IndexError, TypeError):
        return jsonify({"error": "Invalid index"}), 400
    




@app.route("/workouthistory", methods=["POST"])
def add_workout():
    data = request.get_json()
    prompt = data.get("prompt")
    workouts = data.get("workouts", [])

    if not prompt or not workouts:
        return jsonify({"error": "missing prompt or workouts"}), 400

    new_entry = WorkoutHistory(prompt=prompt, workout_data=workouts)
    db.session.add(new_entry)
    db.session.commit()
    print(f"✅ Saved workout for prompt: {prompt}")
    return jsonify({"message": "workout saved"}), 201

@app.route("/workouthistory", methods=["GET"])
def get_history():
    history = WorkoutHistory.query.order_by(WorkoutHistory.timestamp.desc()).all()
    return jsonify([entry.to_dict() for entry in history])

@app.route("/workouthistory/<int:id>", methods=["DELETE"])
def delete_workout_from_history(id):
    workout = WorkoutHistory.query.get_or_404(id)
    db.session.commit()

    try:
        db.session.delete(workout)
        return jsonify({"message": "deleted from workout history"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete workout: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)