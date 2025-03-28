import re

def get_filters():
    return {
        "muscles": [],
        "diff": None,
        "equip": None,
        "count": 10,
        "sets": 3,
        "reps": 10
    }

filters = get_filters()

def word_to_number(prompt):
    words_to_number = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20
    }

    words = prompt.lower().split()
    prompt = " ".join(str(words_to_number[word]) if word in words_to_number else word for word in words)
    return prompt

def number_to_muscle_group_pattern(prompt):

    each_pattern = r"\b(\d{1,2})\s+(?:per|of\s+each|of\s+every|for\s+each|for\s+every|each|every)(\s+(muscle|group|one))?\b"
    number_pattern = r"\b(\d{1,2})\s+(glutes?|quads?|hams?|hamstrings?|biceps?|triceps?|shoulders?|chest|back|abs|obliques|core|arms?|legs?|anterior|posterior|lateral)\b"
    extra_pattern = r"\b(\d{1,2})\s+(?:of\s+(?:them|which)|for|per)\s+(glutes?|quads?|hams?|hamstrings?|biceps?|triceps?|shoulders?|chest|back|abs|obliques|core|arms?|legs?|anterior|posterior|lateral)\b"

    match_each = re.search(each_pattern, prompt)
    if match_each:
        per_count = int(match_each.group(1))
        return True, { "type": "each", "count_per_muscle": per_count, "total": None } 

    match_muscles = re.findall(number_pattern, prompt)
    match_muscles += re.findall(extra_pattern, prompt)
    print("Matched muscle groups:", match_muscles)

    if match_muscles:
        dist = {}
        total = 0
        for count, muscle in match_muscles:
            count = int(count)
            muscle = muscle.lower()
            dist[muscle] = dist.get(muscle, 0) + count
            total += count
        print("Extracted dist:", dist)
        return True, { "type": "specific", "distribution": dist, "total": total }

    return False, None

def sets_and_reps(prompt, filters):
    sets_pattern = r"(\d{1,2})\s*sets?"
    reps_pattern = r"(\d{1,2})\s*reps?"
    combined_pattern = r"(\d{1,2})\s*[xX×]\s*(\d{1,2})"

    match = re.search(combined_pattern, prompt)
    if match:
        filters["sets"] = int(match.group(1))
        filters["reps"] = int(match.group(1))
        prompt = prompt.replace(match.group(0), "")
        return prompt
    
    match_sets = re.search(sets_pattern, prompt)
    match_reps = re.search(reps_pattern, prompt)

    if match_sets:
        filters["sets"] = int(match_sets.group(1))
        prompt = prompt.replace(match_sets.group(0), "")

    if match_reps:
        filters["reps"] = int(match_reps.group(1))
        prompt = prompt.replace(match_reps.group(0), "")
    
    return prompt
    