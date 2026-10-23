import json
import os

PROGRAMS_FILE = "workout_programs.json"

DEFAULT_PROGRAMS = {
    "26X": {
        "Mandag": {
            "title": "Push 1",
            "extra": "+ Mavetræning",
            "exercises": [
                ["Incline chest press", "3 × 6-8"],
                ["Up-rope flyer", "3 × 6-8"],
                ["Fly machine", "3 × 8-10"],
                ["Triceps pushdown ropes", "3 × 10-12"]
            ]
        },
        "Tirsdag": {
            "title": "Pull 1",
            "extra": "",
            "exercises": [
                ["Lat-pulldown cable machine", "3 × 8-10"],
                ["Cable rows", "3 × 6-8"],
                ["Back fly cable tower", "3 × 8-10"],
                ["Seated lateral raises", "3 × 10-12"],
                ["Preacher curls", "3 × 8-10"]
            ]
        },
        "Onsdag": {
            "title": "Ben 1",
            "extra": "",
            "exercises": [
                ["Leg-press", "3 × 8-10"],
                ["Split squat", "3 × 6-8"],
                ["Leg Extension", "3 × 8-10"],
                ["Leg curls", "3 × 8-10"],
                ["Calf raises", "3 × 8-10"]
            ]
        },
        "Torsdag": {
            "title": "Push 2",
            "extra": "+ Mavetræning",
            "exercises": [
                ["Bænkpres", "3 × 6-8"],
                ["Shoulder Press dumbbell", "3 × 8-10"],
                ["Incline dumbbell fly", "3 × 8-10"],
                ["Triceps pushdown rod", "3 × 10-12"]
            ]
        },
        "Fredag": {
            "title": "Pull 2",
            "extra": "",
            "exercises": [
                ["Barbell rows", "3 × 6-8"],
                ["Bicep Lat-pulldown cable machine", "3 × 8-10"],
                ["Straight-arm cable pulldown", "3 × 10-12"],
                ["Seated incline bicep curl", "3 × 8-10"]
            ]
        },
        "Søndag": {
            "title": "Ben 2",
            "extra": "",
            "exercises": [
                ["Hack squad", "3 × 6-8"],
                ["Rumænsk Dødløft", "3 × 8-10"],
                ["Hip abductor and adductor machine", "3 × 8-10"],
                ["Leg Extension", "3 × 8-10"],
                ["Leg curl", "3 × 8-10"]
            ]
        }
    }
}

def load_programs() -> dict:
    if not os.path.exists(PROGRAMS_FILE):
        save_programs(DEFAULT_PROGRAMS)
        return DEFAULT_PROGRAMS
    try:
        with open(PROGRAMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PROGRAMS

def save_programs(programs: dict):
    with open(PROGRAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=4, ensure_ascii=False)

WORKOUT_PROGRAMS = load_programs()