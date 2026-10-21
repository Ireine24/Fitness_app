WORKOUT_PROGRAMS = {
    "26X": {
        "Mandag": {
            "title": "Push 1",
            "extra": "+ Mavetræning",
            "exercises": [
                ("Incline chest press", "3 × 6-8"),
                ("Up-rope flyer", "3 × 6-8"),
                ("Fly machine", "3 × 8-10"),
                ("Triceps pushdown ropes", "3 × 10-12"),
            ]
        },
        "Tirsdag": {
            "title": "Pull 1",
            "extra": "",
            "exercises": [
                ("Lat-pulldown cable machine", "3 × 8-10"),
                ("Cable rows", "3 × 6-8"),
                ("Back fly cable tower", "3 × 8-10"),
                ("Seated lateral raises", "3 × 10-12"),
                ("Preacher curls", "3 × 8-10"),
            ]
        },
        "Onsdag": {
            "title": "Ben 1",
            "extra": "",
            "exercises": [
                ("Leg-press", "3 × 8-10"),
                ("Split squat", "3 × 6-8"),
                ("Leg Extension", "3 × 8-10"),
                ("Leg curls", "3 × 8-10"),
                ("Calf raises", "3 × 8-10"),
            ]
        },
        "Torsdag": {
            "title": "Push 2",
            "extra": "+ Mavetræning",
            "exercises": [
                ("Bænkpres", "3 × 6-8"),
                ("Shoulder Press dumbbell", "3 × 8-10"),
                ("Incline dumbbell fly", "3 × 8-10"),
                ("Triceps pushdown rod", "3 × 10-12"),
            ]
        },
        "Fredag": {
            "title": "Pull 2",
            "extra": "",
            "exercises": [
                ("Barbell rows", "3 × 6-8"),
                ("Bicep Lat-pulldown cable machine", "3 × 8-10"),
                ("Straight-arm cable pulldown", "3 × 10-12"),
                ("Seated incline bicep curl", "3 × 8-10"),
            ]
        },
        "Søndag": {
            "title": "Ben 2",
            "extra": "",
            "exercises": [
                ("Hack squad", "3 × 6-8"),
                ("Rumænsk Dødløft", "3 × 8-10"),
                ("Hip abductor and adductor machine (Supersæt)", "3 × 8-10"),
                ("Leg Extension", "3 × 8-10"),
                ("Leg curl", "3 × 8-10"),
            ]
        }
    },
    "Fiktivt 3-Dages Overkrop/Underkrop Program": {
        "Mandag": {
            "title": "Overkrop Styrke",
            "extra": "+ Core",
            "exercises": [
                ("Barbell Bench Press", "3 × 5-6"),
                ("Barbell Row", "3 × 5-6"),
                ("Standing Overhead Press", "3 × 6-8"),
                ("Weighted Pull-ups", "3 × 6-8"),
            ]
        },
        "Onsdag": {
            "title": "Underkrop Hypertrofi",
            "extra": "",
            "exercises": [
                ("Barbell Squat", "3 × 8-10"),
                ("Romanian Deadlift", "3 × 8-10"),
                ("Bulgarian Split Squat", "3 × 10-12"),
                ("Seated Calf Raises", "4 × 12-15"),
            ]
        },
        "Fredag": {
            "title": "Fullbody Overload",
            "extra": "+ Arm-supersæt",
            "exercises": [
                ("Incline Dumbbell Press", "3 × 8-10"),
                ("Lat Pulldown", "3 × 8-10"),
                ("Dumbbell Lateral Raises", "3 × 12-15"),
                ("Barbell Bicep Curls", "3 × 10-12"),
            ]
        }
    }
}

# For bagudkompatibilitet med resten af appen
WORKOUT_PROGRAM = WORKOUT_PROGRAMS["26X"]