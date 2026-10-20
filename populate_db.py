import sqlite3

def populate():
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    
    # Opret tabellen hvis den ikke findes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dag TEXT NOT NULL,
            oevelse_navn TEXT NOT NULL,
            saet_reps TEXT NOT NULL
        )
    """)
    
    # Ryd evt. gamle data, så vi undgår dubletter
    cursor.execute("DELETE FROM exercises")

    # Dine data fra skemaet
    program_data = [
        # Mandag (Push 1 + Mavetræning)
        ("Mandag", "Incline chest press (+ Mavetræning)", "3 × 6-8"),
        ("Mandag", "Up-rope flyer", "3 × 6-8"),
        ("Mandag", "Fly machine", "3 × 8-10"),
        ("Mandag", "Triceps pushdown ropes", "3 × 10-12"),
        
        # Tirsdag (Pull 1)
        ("Tirsdag", "Lat-pulldown cable machine", "3 × 8-10"),
        ("Tirsdag", "Cable rows", "3 × 6-8"),
        ("Tirsdag", "Back fly cable tower", "3 × 8-10"),
        ("Tirsdag", "Seated lateral raises", "3 × 10-12"),
        ("Tirsdag", "Preacher curls", "3 × 8-10"),

        # Onsdag (Ben 1)
        ("Onsdag", "Leg-press", "3 × 8-10"),
        ("Onsdag", "Split squat", "3 × 6-8"),
        ("Onsdag", "Leg Extension", "3 × 8-10"),
        ("Onsdag", "Leg curls", "3 × 8-10"),
        ("Onsdag", "Calf raises", "3 × 8-10"),

        # Torsdag (Push 2 + Mavetræning)
        ("Torsdag", "Bænkpres (+ Mavetræning)", "3 × 6-8"),
        ("Torsdag", "Shoulder Press dumbbell", "3 × 8-10"),
        ("Torsdag", "Incline dumbbell fly", "3 × 8-10"),
        ("Torsdag", "Triceps pushdown rod", "3 × 10-12"),

        # Fredag (Pull 2)
        ("Fredag", "Barbell rows", "3 × 6-8"),
        ("Fredag", "Bicep Lat-pulldown cable machine", "3 × 8-10"),
        ("Fredag", "Straight-arm cable pulldown", "3 × 10-12"),
        ("Fredag", "Seated incline bicep curl", "3 × 8-10"),

        # Søndag (Ben 2)
        ("Søndag", "Hack squad", "3 × 6-8"),
        ("Søndag", "Rumænsk Dødløft", "3 × 8-10"),
        ("Søndag", "Supersæt: Hip abductor and adductor machine", "3 × 8-10"),
        ("Søndag", "Leg Extension", "3 × 8-10"),
        ("Søndag", "Leg curl", "3 × 8-10")
    ]

    cursor.executemany("""
        INSERT INTO exercises (dag, oevelse_navn, saet_reps) 
        VALUES (?, ?, ?)
    """, program_data)
    
    conn.commit()
    conn.close()
    print("Træningsprogrammet er indsat i databasen!")

if __name__ == "__main__":
    populate()