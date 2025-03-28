import re
from collections import Counter
from models import db, Workout
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from helperfunctions import word_to_number, number_to_muscle_group_pattern, sets_and_reps, get_filters

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


filters = get_filters()



def prompt_filters(prompt):
    filters = {
        "muscles": [],
        "diff": None,
        "equip": None,
        "count": 10,
        "sets": 3,
        "reps": 10
    }
    prompt = word_to_number(prompt)

    prompt = sets_and_reps(prompt, filters)

    # matched_muscles = set()

    for group in workout_type.values(): 
        for muscle, keywords in group.items():
            if any(word in prompt for word in keywords):
                filters["muscles"].append(muscle)

    # if matched_muscles:
    #     filters["muscles"] = list(dict.fromkeys(filters["muscles"]))

    if any(phrase in prompt for phrase in ["upper", "upper body", "upperbody"]):
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
    return filters


def get_filtered_workout(filters, prompt):
    print("🔍 Filters received:", filters)
    query = db.session.query(Workout)

    exclusion_keywords = ["no", "not", "without", "exclude", "avoid", "skip", "except for", "don't want", "dont want"]

    def extract_excluded_muscles(prompt):
        excluded = []
        prompt = prompt.lower()
        for group in workout_type.values():
            for muscle, aliases in group.items():
                for alias in aliases:
                    for kw in exclusion_keywords:
                        pattern = rf"{kw}\s+(the\s)?{alias}"
                        if re.search(pattern, prompt):
                            excluded.append(muscle)
        return list(set(excluded))
    
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

    for w in all_results:
        if filters.get("sets"):
            w.sets = filters["sets"]
        if filters.get("reps"):
            w.reps = filters["reps"]

    

    def ratio_filters(data, muscles, count, prompt):
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

        excluded_muscles = extract_excluded_muscles(prompt)

        filters["muscles"] = [m for m in filters["muscles"] if m not in excluded_muscles]

        if muscle_group == "upperbody":
            muscles = [m for m in muscles if m in workout_type["Upper"]]
        elif muscle_group == "legs":
            muscles = [m for m in muscles if m in workout_type["Legs"]]
        elif muscle_group == "core":
            muscles = [m for m in muscles if m in workout_type["Core"]]
         
        def get_muscle_distribution(muscles, count, order):
                muscle_weights = Counter([m for m in order if m in muscles])
                total_weight = sum(muscle_weights.values())

                distribution = {}
                for muscle, weight in muscle_weights.items():
                    raw = (weight / total_weight) * count
                    distribution[muscle] = int(raw)

                while sum(distribution.values()) < count:
                    for muscle in distribution:
                        distribution[muscle] += 1
                        if sum(distribution.values()) == count:
                            break

                return distribution
        
        def clean_prompt_for_priority(prompt, excluded):
            cleaned = prompt
            for muscle in excluded:
                for alias in sum([v for k, v in workout_type["Upper"].items() if k == muscle], []):
                    for kw in exclusion_keywords:
                        pattern = rf"{kw}\s+(the\s+)?{alias}"
                        cleaned = re.sub(pattern, "", cleaned)
            return cleaned
        
        cleaned_prompt = clean_prompt_for_priority(prompt, excluded_muscles)       
        focus_keywords = ["focus", "emphasize", "prioritize", "mostly", "mainly", "grow", "build", "tone", "lots of", "lots", "lotta", "lot of", "alot of", "a lot of"]

        match muscle_group:
            case "fullbody":
                if any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "chest" in cleaned_prompt:
                    priority = ["back", "chest", "back", "chest", "glutes", "quads", "anterior", "abs", "hams", "biceps", "triceps", "obliques"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "upper" in cleaned_prompt or "upperbody" in cleaned_prompt:
                    priority = ["back", "chest", "back", "chest",  "anterior", "glutes", "quads", "abs", "hams", "biceps", "triceps", "obliques"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "leg" in cleaned_prompt and "core" in cleaned_prompt:
                    priority = ["glutes", "quads", "hams", "glutes", "abs", "obliques", "lower_back", "back", "chest", "biceps", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arm" in cleaned_prompt and "core" in cleaned_prompt:
                    priority = ["biceps", "triceps", "abs", "obliques", "lower_back", "back", "chest", "quads", "glutes"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "glute" in cleaned_prompt and "abs" in cleaned_prompt:
                    priority = ["glutes", "glutes", "abs", "abs", "quads", "hams", "back", "chest", "biceps", "triceps", "obliques"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "arm" in cleaned_prompt:
                    priority = ["chest", "triceps", "chest", "biceps", "back", "glutes", "quads", "abs"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulder" in cleaned_prompt and "arm" in cleaned_prompt:
                    priority = ["anterior", "lateral", "posterior", "biceps", "triceps", "chest", "back", "glutes", "quads", "abs", "hams"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulder" in cleaned_prompt:
                    priority = ["anterior", "lateral", "posterior", "chest", "back", "glutes", "quads", "abs", "hams", "biceps", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "leg" in cleaned_prompt:
                    priority = ["glutes", "quads", "hams", "glutes", "chest", "back", "abs", "anterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "core" in cleaned_prompt:
                    priority = ["abs", "obliques", "lower_back", "abs", "chest", "glutes", "back", "quads"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arm" in cleaned_prompt:
                    priority = ["biceps", "triceps", "biceps", "triceps", "chest", "back", "glutes", "quads", "anterior", "abs"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "glute" in cleaned_prompt:
                    priority = ["glutes", "glutes", "quads", "hams", "abs", "back", "chest"]
                else:
                    priority = ["back", "chest", "anterior", "glutes", "quads", "abs", "hams", "biceps", "triceps", "obliques"]

            case "legs":
                if any(word in cleaned_prompt for word in focus_keywords) and "hams" in cleaned_prompt and "glutes" in cleaned_prompt :
                    priority = ["glutes", "glutes", "hams", "hams", "quads"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "quads" in cleaned_prompt and "glutes" in cleaned_prompt:
                    priority = ["glutes", "glutes", "quads", "quads", "hams"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "quads" in cleaned_prompt and "hams" in cleaned_prompt:
                    priority = ["quads", "quads", "hams", "hams", "glutes"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "quads" in cleaned_prompt:
                    priority = ["quads", "quads", "glutes", "hams"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "hams" in cleaned_prompt:
                    priority = ["hams", "hams", "quads", "glutes"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "glutes" in cleaned_prompt:
                    priority = ["glutes", "glutes", "hams", "quads"]
                else:
                    priority = ["glutes", "hams", "quads"]

            case "upperbody":
                #backfiltering
                if any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "chest" in cleaned_prompt:
                    priority = ["chest", "chest", "back", "back", "posterior", "anterior", "biceps", "lateral", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "shoulders" in cleaned_prompt:
                    priority = ["back", "back", "posterior", "anterior", "chest", "lateral", "biceps", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "arms" in cleaned_prompt:
                    priority = ["back", "back", "biceps", "biceps", "triceps", "chest", "anterior", "lateral", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "anterior" in cleaned_prompt:
                    priority = ["back", "back", "anterior", "anterior", "chest", "biceps", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "lateral" in cleaned_prompt:
                    priority = ["back", "back", "lateral", "lateral", "chest", "anterior", "biceps", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["back", "back", "posterior", "posterior", "chest", "anterior", "biceps", "triceps", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "biceps" in cleaned_prompt:
                    priority = ["back", "back", "biceps", "biceps", "chest", "anterior", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "triceps" in cleaned_prompt:
                    priority = ["back", "back", "triceps", "triceps", "chest", "anterior", "lateral", "biceps", "posterior"]
                #chestfiltering
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "shoulders" in cleaned_prompt:
                    priority = ["chest", "chest", "posterior", "anterior", "back", "lateral", "biceps", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "arms" in cleaned_prompt:
                    priority = ["chest", "chest", "biceps", "biceps", "triceps", "back", "anterior", "lateral", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "anterior" in cleaned_prompt:
                    priority = ["chest", "chest", "anterior", "anterior", "back", "biceps", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "lateral" in cleaned_prompt:
                    priority = ["chest", "chest", "lateral", "lateral", "back", "anterior", "biceps", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["chest", "chest", "posterior", "posterior", "back", "anterior", "biceps", "triceps", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "biceps" in cleaned_prompt:
                    priority = ["chest", "chest", "biceps", "biceps", "back", "anterior", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "triceps" in cleaned_prompt:
                    priority = ["chest", "chest", "triceps", "triceps", "back", "anterior", "lateral", "biceps", "posterior"]
                #shoulders and arms filtering
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt and "arms" in cleaned_prompt:
                    priority = ["anterior", "lateral", "biceps", "biceps", "triceps", "back", "anterior", "lateral", "posterior", "chest"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arms" in cleaned_prompt and "anterior" in cleaned_prompt:
                    priority = ["triceps", "biceps", "anterior", "anterior", "back", "biceps", "triceps", "chest", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arms" in cleaned_prompt and "lateral" in cleaned_prompt:
                    priority = ["biceps", "triceps", "lateral", "lateral",  "biceps", "triceps", "chest", "back", "anterior", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arms" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["biceps", "triceps", "posterior", "posterior", "biceps", "triceps", "back", "chest", "anterior", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt and "biceps" in cleaned_prompt:
                    priority = ["anterior", "lateral", "biceps", "biceps", "back", "chest", "anterior", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt and "triceps" in cleaned_prompt:
                    priority = ["anterior", "lateral", "triceps", "triceps", "back", "chest", "anterior", "lateral", "biceps", "posterior"]
                #singlefocusfiltering
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt:
                    priority = ["back", "back", "back", "chest", "anterior", "biceps", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt:
                    priority = ["chest", "chest", "chest", "back", "anterior", "biceps", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt:
                    priority = ["anterior", "lateral", "posterior", "back", "chest", "anterior", "biceps", "lateral", "triceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "arms" in cleaned_prompt:
                    priority = ["biceps", "triceps", "back", "chest", "anterior", "biceps", "lateral", "triceps", "posterior"]
                else:
                    priority = ["chest", "back", "anterior", "biceps", "lateral", "triceps", "posterior"]

            case "shoulders":
                if any(word in cleaned_prompt for word in focus_keywords) and "anterior" in cleaned_prompt and "lateral" in cleaned_prompt:
                    priority = ["anterior", "lateral", "anterior", "lateral", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "anterior" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["anterior", "posterior", "anterior", "posterior", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "lateral" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["posterior", "lateral", "posterior", "lateral", "anterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "anterior" in cleaned_prompt:
                    priority = ["anterior", "anterior", "lateral", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "lateral" in cleaned_prompt:
                    priority = ["lateral", "lateral", "anterior", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "posterior" in cleaned_prompt:
                    priority = ["posterior", "posterior", "lateral", "anterior"]
                else:
                    priority = ["anterior", "lateral", "posterior"]

            case "arms":
                if any(word in cleaned_prompt for word in focus_keywords) and "biceps" in cleaned_prompt:
                    priority = ["biceps", "biceps", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "triceps" in cleaned_prompt:
                    priority = ["triceps", "triceps", "biceps"]
                else:
                    priority = ["biceps", "triceps"]

            case "push":
                if any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "shoulders" in cleaned_prompt:
                    priority = ["chest", "lateral", "chest", "anterior", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt and "triceps" in cleaned_prompt:
                    priority = ["chest", "triceps", "chest", "triceps", "lateral"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt and "triceps" in cleaned_prompt:
                    priority = ["triceps", "lateral", "anterior", "triceps", "chest"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "chest" in cleaned_prompt:
                    priority = ["chest", "chest", "anterior", "lateral", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "shoulders" in cleaned_prompt:
                    priority = ["lateral", "lateral", "anterior", "anterior", "chest", "triceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "triceps" in cleaned_prompt:
                    priority = ["triceps", "triceps", "lateral", "anterior", "chest"]
                else:
                    priority = ["chest", "anterior", "lateral", "triceps"]

            case "pull":
                if any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "biceps" in cleaned_prompt:
                    priority = ["back", "biceps", "back", "biceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["back", "posterior", "back", "posterior", "biceps"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "biceps" in cleaned_prompt and "posterior" in cleaned_prompt:
                    priority = ["posterior", "biceps", "posterior", "biceps", "back"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "back" in cleaned_prompt:
                    priority = ["back", "back", "biceps", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "biceps" in cleaned_prompt:
                    priority = ["biceps", "biceps", "back", "posterior"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "posterior" in cleaned_prompt:
                    priority = ["posterior", "posterior", "biceps", "back"]
                else:
                    priority = ["back", "biceps", "posterior"]

            case "core":
                if any(word in cleaned_prompt for word in focus_keywords) and "abs" in cleaned_prompt and "obliques" in cleaned_prompt:
                    priority = ["abs", "obliques", "abs", "obliques", "lower_back"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "abs" in cleaned_prompt and "lower_back" in cleaned_prompt:
                    priority = ["abs", "lower_back", "abs", "lower_back", "obliques"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "obliques" in cleaned_prompt and "lower_back" in cleaned_prompt:
                    priority = ["lower_back", "obliques", "lower_back", "obliques", "abs"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "abs" in cleaned_prompt:
                    priority = ["abs", "abs", "obliques", "lower_back"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "obliques" in cleaned_prompt:
                    priority = ["obliques", "obliques", "abs", "lower_back"]
                elif any(word in cleaned_prompt for word in focus_keywords) and "lower_back" in cleaned_prompt:
                    priority = ["lower_back", "lower_back", "obliques", "abs"]
                else:
                    priority = ["abs", "obliques", "lower_back"]

            case "custom":
                priority = (muscles * (count // len(muscles))) + muscles[:(count % len(muscles))]

        priority = [m for m in priority if m not in excluded_muscles]
        print(priority)
           

        matched, result = number_to_muscle_group_pattern(prompt)

        if matched:
            
            if result["type"] == "each":
                distribution = {muscle: result["count_per_muscle"] for muscle in muscles}
                count = sum(distribution.values())
            elif result["type"] == "specific":
                print("Matched distribution before fill:", result["distribution"])
                distribution = result["distribution"]
                

                reminder = count - sum(distribution.values())
                if reminder > 0:
                        remaining_muscles = [m for m in muscles if m not in result["distribution"]]
                        if remaining_muscles:
                            for i in range(reminder):
                                muscle = remaining_muscles[i % len(remaining_muscles)]
                                distribution[muscle] = distribution.get(muscle, 0) + 1
        else:
            distribution = get_muscle_distribution(muscles, count, priority)
        print("Final distribution:", distribution)
        for muscle, num in distribution.items():
            print(f"  - {muscle}: {num} workout(s)")


        selected = []
        for muscle, num in distribution.items():
            matches = [
                w for w in data 
                if (
                    (isinstance(w.targeted_muscles, list) and muscle in w.targeted_muscles)
                    or (isinstance(w.targeted_muscles, str) and muscle in w.targeted_muscles.lower())
                )
                and not any(ex in w.targeted_muscles.lower() for ex in excluded_muscles)
            ]
            print(f"🧪 [{muscle}] → wanted {num}, found {len(matches)} matches")
            selected.extend(matches[:num])
            
        seen = set()
        unique_selected = []
        for w in selected:
            if w.id not in seen:
                unique_selected.append(w)
                seen.add(w.id)
        return unique_selected     

    full_query = ratio_filters(all_results, filters["muscles"], filters["count"], prompt)
    return full_query