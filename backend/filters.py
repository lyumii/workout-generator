import re
from models import db, Workout
from sqlalchemy import or_
from sqlalchemy.sql.expression import func

def prompt_filters(prompt):
    prompt = prompt.lower()
    workout_type = {
        "Upper": {
            "biceps": ["biceps", "guns", "bi's", "bis", "front arm", "front arms", "bicep", "pipes"],
            "triceps": [ "triceps", "back arm", "back arms", "tris", "tri's", "tricep", "horseshoe"],
            "back": ["teres", "latissimus", "lats", "back", "traps", "trapezius", "lat", "rhomboids"],
            "chest": ["chest", "pecs", "pectorals", "boobs", "boob"],
            "anterior": ["front delts", "front delt", "anterior delt", "anterior delts"],
            "lateral": ["lat delts", "lat delt", "lateral delts", "lateral delt", "side delt", "side delts"],
            "posterior": ["rear delt", "rear delts", "posterior delt", "posterior delts"]
        },
        "Legs": {
            "glutes": ["butt", "ass", "booty", "glutes", "glute"],
            "quads": ["quads", "quadriceps"],
            "hams": ["hamstrings", "hams"]
        },
        "Core": {
            "abs": ["abs", "abdominals", "six pack"],
            "obliques": ["obliques", "sides"],
            "lower_back": ["lower back", "erector spinae", "lumbar", "spinal erectors"]
        }
    }

    difficulty_levels = {
        "easy": ["beginner", "easy", "simple"],
        "medium": ["medium", "intermediate"],
        "hard": ["hard", "advanced", "difficult"]
    }

    equipment = {
        "bodyweight": ["bodyweight", "just body", "no weights"],
        "dumbbell": ["dumbbells", "dumbbell"],
        "barbell": ["barbell", "barbells"],
        "cable": ["cable", "cables"]
    }

    filters = {
        "muscles": [],
        "diff": None,
        "equip": None,
        "count": 10
    }


    matched_muscles = set()
    for group in workout_type.values(): 
        for muscle, keywords in group.items():
            if any(word in prompt for word in keywords):
                filters["muscles"].append(muscle)

    if matched_muscles:
        filters["muscles"] = list(dict.fromkeys(filters["muscles"]))

    if any(phrase in prompt for phrase in ["upper", "upper body"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(workout_type["Upper"].keys())
    if any(phrase in prompt for phrase in ["push"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(["chest", "triceps", "anterior", "lateral"])
    if any(phrase in prompt for phrase in ["pull"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(["back", "biceps", "posterior"])
    if any(phrase in prompt for phrase in ["leg", "legs", "lower body"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(workout_type["Legs"].keys()) 
    if any(phrase in prompt for phrase in ["core", "tummy", "trunk", "stomach"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(workout_type["Core"].keys())
    if any(phrase in prompt for phrase in ["delt", "delts", "shoulder", "shoulders"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(["lateral", "posterior", "anterior"])
    if any(phrase in prompt for phrase in ["arm", "arms"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(["biceps", "triceps"])
    if any(phrase in prompt for phrase in ["full body", "fullbody"]):
        for subgroups in workout_type.values():
            filters["muscles"].extend(subgroups.keys())
    
    filters["muscles"] = list(dict.fromkeys(filters["muscles"]))


    for diff, keywords in difficulty_levels.items():
        if any(keyword in prompt for keyword in keywords):
            filters["diff"] = diff

    for equip, keywords in equipment.items():
        if any(keyword in prompt for keyword in keywords):
            filters["equip"] = equip

    
    match = re.search(r"\b\d+\b", prompt)
    if match:
        filters["count"] = int(match.group())
    
    print("Prompt lowercased:", prompt)
    for muscle, keywords in workout_type.items():
        print(f"Checking {muscle} with keywords {keywords}")
    if any(kw in prompt for kw in keywords):
        print(f"✅ Match found for muscle: {muscle}")
        filters["muscles"].append(muscle)
    

    return filters


def get_filtered_workout(filters):
    print("🔍 Filters received:", filters)
    query = db.session.query(Workout)
    if filters["muscles"]:
        muscle_conditions = [
            Workout.targeted_muscles.ilike(f"%{muscle}%") for muscle in filters["muscles"]
        ]
        query = query.filter(or_(*muscle_conditions))

    if filters["diff"]:
        query = query.filter(Workout.difficulty == filters["diff"])

    if filters["equip"]:
        query = query.filter(Workout.equipment.ilike(f"%{filters['equip']}%"))
    query = query.order_by(func.random()) 
    all_results = query.all()

    def ratio_filters(data, muscles, count):
        if not muscles:
            print("⚠️ No muscles provided — returning empty list")
            return []
        def get_muscle_grp(muscles):
            if set(muscles) == {
                'biceps', 'triceps', 'back', 'chest', 'anterior', 'lateral',
                'posterior', 'glutes', 'quads', 'hams', 'abs', 'obliques', 'lower_back'
            }:
                return "fullbody"
            elif set(muscles) == {"glutes", "quads", "hams"}:
                return "legs"
            elif set(muscles) == {"back", "chest", "anterior", "lateral", "posterior", "biceps", "triceps"}:
                return "upperbody"
            elif set(muscles) == {"anterior", "posterior", "lateral"}:
                return "shoulders"
            elif set(muscles) == {"biceps", "triceps"}:
                return "arms"
            elif set(muscles) == {"abs", "obliques", "lower_back"}:
                return "core"
            elif set(muscles) == {"chest", "triceps", "anterior", "lateral"}:
                return "push"
            elif set(muscles) == {"back", "biceps", "posterior"}:
                return "pull"
            else:
                return "custom"

            
        muscle_group = get_muscle_grp(muscles) 
        print("💡 muscle_group:", muscle_group)   
        def get_muscle_distribution(muscles, count, order):
                seen = set()
                prioritized = []
                for m in order:
                    if m in muscles and m not in seen:
                        prioritized.append(m)
                        seen.add(m)

                if count <= len(prioritized):
                    return {m: 1 for m in prioritized[:count]}

                base = count // len(prioritized)
                extra = count % len(prioritized)

                distribution = {}
                for i, m in enumerate(prioritized):
                    distribution[m] = base + (1 if i < extra else 0)

                return distribution

        match muscle_group:
            case "fullbody":
                priority = ["back", "chest", "anterior", "glutes", "quads", "abs", "hams", "biceps", "triceps", "obliques"]
            case "legs":
                priority = ["glutes", "quads", "hams"]
            case "upperbody":
                priority = ["chest", "back", "anterior", "biceps", "lateral", "triceps", "posterior"]
            case "shoulders":
                priority = ["anterior", "lateral", "posterior"]
            case "arms":
                priority = ["biceps", "triceps"]
            case "push":
                priority = ["chest", "anterior", "lateral", "triceps"]
            case "pull":
                priority = ["back", "posterior", "biceps"]
            case "core":
                priority = ["abs", "obliques", "lower_back"]
            case "custom":
                priority = (muscles * (count // len(muscles))) + muscles[:(count % len(muscles))]

        print(priority)
            

        distribution = get_muscle_distribution(muscles, count, priority)
        print("🎯 Distribution breakdown:")
        for muscle, num in distribution.items():
            print(f"  - {muscle}: {num} workout(s)")


        selected = []
        for muscle, num in distribution.items():
            matches = [
                w for w in data 
                if isinstance(w.targeted_muscles, list) and muscle in w.targeted_muscles
                or isinstance(w.targeted_muscles, str) and muscle in w.targeted_muscles.lower()
            ]
            print(f"IDs: {[w.id for w in matches[:num]]}")
            print(f"→ Adding {num} workout(s) for '{muscle}' from {len(matches)} matches")
            selected.extend(matches[:num])
        seen = set()
        unique_selected = []
        for w in selected:
            if w.id not in seen:
                unique_selected.append(w)
                seen.add(w.id)
        return unique_selected
        
        # print(selected)
        # return selected         

    full_query = ratio_filters(all_results, filters["muscles"], filters["count"])
    print("🧪 Final SQL query:", str(query))
    return full_query