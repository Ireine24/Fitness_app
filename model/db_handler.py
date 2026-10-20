import sqlite3
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_path: str = "fitness.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Tabel til træningssæt og øvelser
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dato TEXT NOT NULL,
                ovelse TEXT NOT NULL,
                vaegt REAL NOT NULL,
                reps INTEGER NOT NULL
            )
        """)
        # Tabel til ugentligt træningsprogram (baseret på ugedage)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dag TEXT NOT NULL,
                oevelse_navn TEXT NOT NULL,
                saet_reps TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def get_program_for_day(self, dag: str) -> list:
        """Henter træningsprogram for en specifik ugedag fra databasen."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT oevelse_navn, saet_reps FROM exercises WHERE dag = ?", 
            (dag,)
        )
        results = cursor.fetchall()
        conn.close()
        return results

    def insert_program_exercise(self, dag: str, oevelse_navn: str, saet_reps: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exercises (dag, oevelse_navn, saet_reps) VALUES (?, ?, ?)",
            (dag, oevelse_navn, saet_reps)
        )
        conn.commit()
        conn.close()