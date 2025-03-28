from app import app
from models import db, Workout



def w(name, type, diff, muscles, equipment):
    return Workout(
        name=name,
        type=type,
        difficulty=diff,
        targeted_muscles=muscles,
        equipment=equipment
    )

workout = [

    #shoulders

    w("Barbell Front Raise", "Upper", "medium", "front, deltoids, anterior, shoulders", "barbell" ),
    w("Barbell Military Press", "Upper", "medium", "front, anterior, deltoid, shoulders", "barbell"),
    w("One Arm Cable Front Raise", "Upper", "easy", "front, deltoids, anterior, shoulders", "cable"),
    w("Seated Cable Shoulder Press", "Upper", "medium", "front, anterior, deltoid, shoulders", "cable"),
    w("Dumbbell Arnold Press", "Upper", "easy", "front, deltoids, anterior, shoulders", "dumbbell"),
    w("Dumbbell Front Raise", "Upper", "easy", "front, anterior, deltoid, shoulders", "dumbbell"),
    w("Dumbbell Shoulder Press", "Upper", "medium", "front, anterior, deltoid, shoulders", "dumbbell"),
    w("Barbell Upright Row", "Upper", "medium", "deltoid, lateral, shoulders, side, lat", "barbell"),
    w("One Arm Cable Lateral Raise", "Upper", "easy", "deltoid, lateral, shoulders, side, lat", "cable"),
    w("Cable Upright Row", "Upper", "medium", "deltoid, lateral, shoulders, side, lat", "cable"),
    w("Cable Y Row", "Upper", "medium", "deltoid, lateral, shoulders, side, lat", "cable"),
    w("Dumbbell Incline Lateral Raise", "Upper", "hard", "deltoid, lateral, shoulders, side, lat", "dumbbell"),
    w("Dumbbell Lateral Raise",  "Upper", "medium", "deltoid, lateral, shoulders, side, lat", "dumbbell"),
    w("Dumbbell Upright Row", "Upper", "medium", "deltoid, lateral, shoulders, side, lat", "dumbbell"),
    w("Barbell Rear Delt Row", "Upper", "medium", "rear, posterior, deltoid, shoulders", "barbell"),
    w("Cable Reverse Fly", "Upper", "medium", "rear, posterior, deltoid, shoulders", "cable"),
    w("Cable Rear Delt Row", "Upper", "easy", "rear, posterior, deltoid, shoulders", "cable"),
    w("Cable Rear Lateral Raise", "Upper", "hard", "rear, posterior, deltoid, shoulders", "cable"),
    w("Dumbbell Rear Lateral Raise", "Upper", "medium", "rear, posterior, deltoid, shoulders", "dumbbell"),
    w("Dumbbell Rear Delt Row", "Upper", "medium", "rear, posterior, deltoid, shoulders", "dumbbell"), 
    w("Seated Rear Lateral Raise", "Upper", "medium", "rear, posterior, deltoid, shoulders", "dumbbell"),
    w("Pike Press", "Upper", "medium", "anterior, deltoid, shoulders", "bodyweight"),
    w("Elevated Pike Press", "Upper", "hard", "anterior, deltoid, shoulders", "bodyweight"),
    w("Suspended Front Raise", "Upper", "hard", "anterior, deltoid, shoulders", "bodyweight"),
    w("Rear Delt Inverted Row", "Upper", "hard", "rear, posterior, deltoid, shoulders", "bodyweight"),

    #arms

    w("Close Grip Bench Press", "Upper", "medium", "triceps brachii, arms", "barbell"),
    w("Lying Triceps Extension (Skull Crusher)", "Upper", "medium", "triceps brachii, arms", "barbell"),
    w("Standing Triceps Extension", "Upper", "medium", "triceps brachii, arms", "barbell"),
    w("Bent-over Triceps Extension", "Upper", "easy", "triceps brachii, arms", "cable"),
    w("Lying Triceps Extension", "Upper", "medium", "triceps brachii, arms", "cable"),
    w("Triceps Pushdown", "Upper", "easy", "triceps brachii, arms", "cable"),
    w("One Arm Triceps Pushdown", "Upper", "medium", "triceps brachii, arms", "cable"),
    w("Triceps Pushdown with V-bar Attachment", "Upper", "medium", "triceps brachii, arms", "cable"),
    w("Triceps Dip", "Upper", "medium", "triceps brachii, arms", "cable"),
    w("Triceps Extension", "Upper", "easy", "triceps brachii, arms", "cable"),
    w("Triceps Extension with Rope", "Upper", "medium", "triceps brachii, arms", "cable"),
    w("Triceps Kickback", "Upper", "easy", "triceps brachii, arms", "dumbbell"),
    w("Lying Triceps Extension", "Upper", "medium", "triceps brachii, arms", "dumbbell"),
    w("One Arm Triceps Extension (on bench)", "Upper", "medium", "triceps brachii, arms", "dumbbell"),
    w("Standing Triceps Extension", "Upper", "medium", "triceps brachii, arms", "dumbbell"),
    w("Bench Dip", "Upper", "easy", "triceps brachii, arms", "bodyweight"),
    w("Close Grip Push-up", "Upper", "medium", "triceps brachii, arms", "bodyweight"),
    w("Incline Close Grip Push-up on Bar", "Upper", "medium", "triceps brachii, arms", "bodyweight"),
    w("Triceps Dip", "Upper", "hard", "triceps brachii, arms", "bodyweight"),
    w("Barbell Curl", "Upper", "medium", "biceps brachii, arms", "barbell"),
    w("Alternating Cable Curl", "Upper", "medium", "biceps brachii, arms", "cable"),
    w("Cable Curl with Stirrups", "Upper", "medium", "biceps brachii, arms", "cable"),
    w("One Arm Cable Curl", "Upper", "medium", "biceps brachii, arms", "cable"),
    w("Dumbbell Curl", "Upper", "easy", "biceps brachii, arms", "dumbbell"),
    w("Incline Dumbbell Curl", "Upper", "hard", "biceps brachii, arms", "dumbbell"),
    w("Inverted Biceps Row", "Upper", "medium", "biceps brachii, arms", "bodyweight"),
    w("Barbell Preacher Curl", "Upper", "medium", "brachialis, arms", "barbell"),
    w("Prone Incline Barbell Curl", "Upper", "medium", "brachialis, arms", "barbell"),
    w("Cable Concentration Curl", "Upper", "medium", "brachialis, arms", "cable"),
    w("Cable Preacher Curl with Stirrups", "Upper", "hard", "brachialis, arms", "cable"),
    w("Dumbbell Concentration Curl", "Upper", "medium", "brachialis, arms", "dumbbell"),
    w("Dumbbell Preacher Curl", "Upper", "medium", "brachialis, arms", "dumbbell"),
    w("Suspended Arm Curl", "Upper", "hard", "brachialis, arms", "bodyweight"),

    #back
    
    w("Bent-over Row", "Upper", "easy, medium", "general back", "barbell"),
    w("Underhand Bent-over Row", "Upper", "medium", "general back", "barbell"),
    w("Barbell Pullover", "Upper", "medium", "latissimus dorsi, teres major, back", "barbell"),
    w("Barbell Shrug", "Upper", "easy, medium", "upper trapezius, levator scapulae, back", "barbell"),
    w("Trap Bar Shrug", "Upper", "medium", "upper trapezius, levator scapulae, back", "barbell"),
    w("Bent-over Row", "Upper", "medium, easy", "general back", "dumbbell"),
    w("Lying Row", "Upper", "medium", "general back", "dumbbell"),
    w("Dumbbell Shrug", "Upper", "medium, easy", "upper trapezius, levator scapulae, back", "dumbbell"),
    w("One Arm Bent-over Row", "Upper", "medium", "general back", "cable"),
    w("Seated Row", "Upper", "medium, easy", "general back", "cable"),
    w("One Arm Straight Back Seated High Row", "Upper", "medium", "general back", "cable"),
    w("Seated Wide Grip Row", "Upper", "medium", "general back", "cable"),
    w("Bent-over Pullover", "Upper", "medium", "latissimus dorsi, teres major,, back", "cable"),
    w("Close Grip Pulldown", "Upper", "medium", "latissimus dorsi, teres major, back", "cable"),
    w("Pulldown", "Upper", "medium, easy", "latissimus dorsi, teres major, back", "cable"),
    w("Underhand Pulldown", "Upper", "medium", "latissimus dorsi, teres major, back", "cable"),
    w("Cable Shrug", "Upper", "medium", "upper trapezius, levator scapulae, back", "cable"),
    w("Cable Shrug with Stirrups", "Upper", "medium", "upper trapezius, levator scapulae, back", "cable"),
    w("Inverted Row", "Upper", "medium", "general back", "bodyweight"),
    w("Inverted Row with Feet Elevated", "Upper", "medium", "general back", "bodyweight"),
    w("Inverted Row on High Bar", "Upper", "medium", "general back", "bodyweight"),
    w("Chin-up", "Upper", "hard", "latissimus dorsi, teres major, back", "bodyweight"),
    w("Pull-up", "Upper", "hard", "latissimus dorsi, teres major, back", "bodyweight"),
    w("Parallel Close Grip Pull-up", "Upper", "hard", "latissimus dorsi, teres major, back", "bodyweight"),
    w("Inverted Shrug", "Upper", "medium", "upper trapezius, levator scapulae, back", "bodyweight"),

    #chest

    w("Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "barbell"),
    w("Decline Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "barbell"),
    w("Incline Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "barbell"),
    w("Bench Press", "Upper", "medium, easy", "chest, pecs, pectoralis", "dumbbell"),
    w("Decline Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "dumbbell"),
    w("Fly", "Upper", "medium, easy", "chest, pecs, pectoralis", "dumbbell"),
    w("Pullover", "Upper", "medium", "chest, pecs, pectoralis", "dumbbell"),
    w("Incline Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "dumbbell"),
    w("Incline Fly", "Upper", "medium", "chest, pecs, pectoralis", "dumbbell"),
    w("Lying Fly", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Seated Fly", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Standing Fly", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Chest Press (Standing)", "Upper", "medium, easy", "chest, pecs, pectoralis", "cable"),
    w("Decline Chest Press", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Incline Bench Press", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Incline Chest Press", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Incline Fly", "Upper", "medium", "chest, pecs, pectoralis", "cable"),
    w("Chest Dip", "Upper", "hard", "chest, pecs, pectoralis", "bodyweight"),
    w("Push-up", "Upper", "easy", "chest, pecs, pectoralis", "bodyweight"),
    w("Archer Push-up", "Upper", "medium", "chest, pecs, pectoralis", "bodyweight"),
    w("Incline Push-up", "Upper", "easy", "chest, pecs, pectoralis", "bodyweight"),
    w("Push-up on Knees", "Upper", "easy", "chest, pecs, pectoralis", "bodyweight"),
    w("Decline Push-up", "Upper", "medium", "chest, pecs, pectoralis", "bodyweight"),
    w("Clap Push-up", "Upper", "hard", "chest, pecs, pectoralis", "bodyweight"),
    w("Depth Push-up", "Upper", "hard", "chest, pecs, pectoralis", "bodyweight"),

    #core

    w("Crunch", "Core", "easy", "core, abs, upper abs", "bodyweight"),
    w("Reverse Crunch", "Core", "easy", "core, abs, lower abs", "bodyweight"),
    w("Leg Raises", "Core", "medium", "core, abs, lower abs", "bodyweight"),
    w("Plank", "Core", "medium", "core, abs", "bodyweight"),
    w("Side Plank", "Core", "medium", "core, obliques", "bodyweight"),
    w("Bird Dog", "Core", "easy", "core, lower back", "bodyweight"),
    w("Superman Hold", "Core", "easy", "core, lower back", "bodyweight"),
    w("Mountain Climbers", "Core", "medium", "core, abs, lower abs", "bodyweight"),
    w("Dead Bug", "Core", "medium", "core, abs", "bodyweight"),
    w("V-Ups", "Core", "hard", "core, abs, upper abs, lower abs", "bodyweight"),
    w("Hollow Body Hold", "Core", "hard", "core, abs, lower abs", "bodyweight"),
    w("Toes to Bar", "Core", "hard", "core, abs, lower abs", "bodyweight"),
    w("Plank to Push-up", "Core", "hard", "core, abs, obliques", "bodyweight"),
    w("Side Plank with Hip Dips", "Core", "hard", "core, obliques", "bodyweight"),
    w("Wall Walk", "Core", "hard", "core, abs, lower back", "bodyweight"),
    w("Cable Woodchopper", "Core", "medium", "core, obliques", "cable"),
    w("Cable Crunch", "Core", "medium", "core, abs, upper abs", "cable"),
    w("Russian Twist with Dumbbell", "Core", "medium", "core, obliques, abs", "dumbbell"),
    w("Weighted Sit-up", "Core", "medium", "core, abs, upper abs", "dumbbell"),
    w("Barbell Rollout", "Core", "hard", "core, abs, lower abs, lower back", "barbell"),

    #glutes 

    w("Barbell Hip Thrust", "Legs", "medium", "glutes, gluteus maximus", "barbell"),
    w("Barbell Squat", "Legs", "medium", "glutes, gluteus maximus", "barbell"),
    w("Barbell Deadlift", "Legs", "medium", "glutes, gluteus maximus", "barbell"),
    w("Barbell Lunge", "Legs", "medium", "glutes, gluteus maximus", "barbell"),
    w("Barbell Step-Up", "Legs", "medium", "glutes, gluteus maximus", "barbell"),
    w("Dumbbell Bulgarian Split Squat", "Legs", "medium", "glutes, gluteus maximus", "dumbbell"),
    w("Dumbbell Deadlift", "Legs", "medium", "glutes, gluteus maximus", "dumbbell"),
    w("Dumbbell Step-Up", "Legs", "medium", "glutes, gluteus maximus", "dumbbell"),
    w("Dumbbell Hip Thrust", "Legs", "medium", "glutes, gluteus maximus", "dumbbell"),
    w("Dumbbell Lateral Lunge", "Legs", "medium", "glutes, gluteus medius", "dumbbell"),
    w("Cable Glute Kickback", "Legs", "medium", "glutes, gluteus maximus", "cable"),
    w("Cable Pull-Through", "Legs", "medium", "glutes, gluteus maximus", "cable"),
    w("Cable Squat", "Legs", "medium", "glutes, gluteus maximus", "cable"),
    w("Cable Single-Leg Romanian Deadlift", "Legs", "medium", "glutes, gluteus maximus", "cable"),
    w("Glute Bridge", "Legs", "easy", "glutes, gluteus maximus", "bodyweight"),
    w("Single-Leg Glute Bridge", "Legs", "medium", "glutes, gluteus maximus", "bodyweight"),
    w("Squat", "Legs", "easy", "glutes, gluteus maximus", "bodyweight"),
    w("Lunge", "Legs", "easy", "glutes, gluteus maximus", "bodyweight"),
    w("Step-Up", "Legs", "easy", "glutes, gluteus maximus", "bodyweight"),
    w("Fire Hydrant", "Legs", "easy", "glutes, gluteus medius", "bodyweight"),
    w("Donkey Kick", "Legs", "easy", "glutes, gluteus maximus", "bodyweight"),
    w("Clamshell", "Legs", "easy", "glutes, gluteus medius", "bodyweight"),
    w("Side-Lying Hip Abduction", "Legs", "easy", "glutes, gluteus medius", "bodyweight"),
    w("Hip Thrust", "Legs", "medium", "glutes, hamstrings, hams", "barbell"),
    w("Dumbbell Hip Thrust", "Legs", "medium", "glutes, hamstrings, hams", "dumbbell"),
    w("Frog Pump", "Legs", "easy", "glutes, hamstrings, hams", "bodyweight"),


    #legs 
    w("Dumbbell Step-Up", "Legs", "medium", "quadriceps, quads", "dumbbell"),
    w("Dumbbell Lunge", "Legs", "medium", "quadriceps, quads", "dumbbell"),
    w("Sissy Squat", "Legs", "hard", "quadriceps, quads", "bodyweight"),
    w("Smith Machine Squat", "Legs", "medium", "quadriceps, quads", "smith machine"),
    w("Cable Squat", "Legs", "medium", "quadriceps, quads", "cable"),
    w("Split Squat", "Legs", "medium", "quadriceps, quads", "bodyweight"),
    w("Wall Sit", "Legs", "easy", "quadriceps, quads", "bodyweight"),
    w("Cyclist Squat", "Legs", "medium", "quadriceps, quads", "barbell"),
    w("Barbell Squat", "Legs", "medium", "quadriceps, quads", "barbell"),
    w("Front Squat", "Legs", "medium", "quadriceps, quads", "barbell"),
    w("Leg Press", "Legs", "medium", "quadriceps, quads", "machine"),
    w("Lunge", "Legs", "easy", "quadriceps, quads", "bodyweight"),
    w("Bulgarian Split Squat", "Legs", "medium", "quadriceps, quads", "bodyweight"),
    w("Step-Up", "Legs", "easy", "quadriceps, quads", "bodyweight"),
    w("Leg Extension", "Legs", "easy", "quadriceps, quads", "machine"),
    w("Goblet Squat", "Legs", "easy", "quadriceps, quads", "dumbbell"),
    w("Romanian Deadlift", "Legs", "medium", "hamstrings, hams", "barbell"),
    w("Stiff-Legged Deadlift", "Legs", "medium", "hamstrings, hams", "barbell"),
    w("Leg Curl", "Legs", "easy", "hamstrings, hams", "machine"),
    w("Glute-Ham Raise", "Legs", "hard", "hamstrings, hams", "bodyweight"),
    w("Good Morning", "Legs", "medium", "hamstrings, hams", "barbell"),
    w("Kettlebell Swing", "Legs", "medium", "hamstrings, hams", "kettlebell"),
    w("Single-Leg Deadlift", "Legs", "medium", "hamstrings, hams", "dumbbell"),
    w("Deadlift", "Legs", "medium", "quadriceps, quads, hamstrings, hams", "barbell"),
    w("Sumo Deadlift", "Legs", "medium", "quadriceps, quads, hamstrings, hams", "barbell"),
    w("Trap Bar Deadlift", "Legs", "medium", "quadriceps, quads, hamstrings, hams", "trap bar"),
    w("Hack Squat", "Legs", "medium", "quadriceps, quads, hamstrings, hams", "machine"),
    w("Seated Leg Curl", "Legs", "easy", "hamstrings, hams", "machine"),
    w("Standing Leg Curl", "Legs", "easy", "hamstrings, hams", "machine"),
    w("Cable Pull-Through", "Legs", "medium", "hamstrings, hams, glutes", "cable"),
    w("Glute Kickback", "Legs", "easy", "hamstrings, hams, glutes", "cable"),
    w("Dumbbell Romanian Deadlift", "Legs", "medium", "hamstrings, hams", "dumbbell"),
    w("Dumbbell Good Morning", "Legs", "medium", "hamstrings, hams", "dumbbell"),
    w("Single-Leg Glute Bridge", "Legs", "medium", "hamstrings, hams, glutes", "bodyweight"),
    w("Hamstring Walkout", "Legs", "medium", "hamstrings, hams", "bodyweight"),

]

with app.app_context():
    db.create_all()
    db.session.add_all(workout)
    db.session.commit()
    print("✅ Seeded workouts into the database.")