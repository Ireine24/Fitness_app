import sqlite3
import pandas as pd


class DatabaseHandler:
    def __init__(self, db_path: str = "fitness.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        """Opretter tabellerne hvis de ikke findes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Træningspas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workout_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dato TEXT NOT NULL UNIQUE,
                    noter TEXT DEFAULT ''
                )
            """)

            # Enkelte løft knyttet til et træningspas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workout_sets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    ovelse TEXT NOT NULL,
                    vaegt REAL NOT NULL,
                    reps INTEGER NOT NULL,
                    estimeret_1rm REAL NOT NULL,
                    noter TEXT DEFAULT '',
                    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE
                )
            """)

            # Kropsvægt
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bodyweight_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dato TEXT NOT NULL,
                    vaegt REAL NOT NULL
                )
            """)
            conn.commit()

    # --- Træningspas og løft ---
    def read_all_sets(self) -> pd.DataFrame:
        """Henter alle registrerede løft sammen med datoen fra passet."""
        query = """
            SELECT s.id AS set_id, w.id AS session_id, w.dato AS "Dato", 
                   s.ovelse AS "Øvelse", s.vaegt AS "Vægt (kg)", 
                   s.reps AS "Reps", s.estimeret_1rm AS "Estimeret 1RM (kg)", 
                   s.noter AS "Noter"
            FROM workout_sets s
            JOIN workout_sessions w ON s.session_id = w.id
            ORDER BY w.dato ASC, s.id ASC
        """
        with self._get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def read_workout_sessions_summary(self) -> pd.DataFrame:
        """Henter en samlet oversigt over hvert enkelt træningspas nummereret opad."""
        query = """
            SELECT 
                w.id AS session_id,
                w.dato AS "Dato",
                COUNT(s.id) AS "Sæt",
                ROUND(TOTAL(s.vaegt * s.reps), 1) AS "Total volumen (kg)",
                ROUND(COALESCE(MAX(s.estimeret_1rm), 0), 1) AS "Maks 1RM (kg)"
            FROM workout_sessions w
            LEFT JOIN workout_sets s ON w.id = s.session_id
            GROUP BY w.id, w.dato
            ORDER BY w.dato ASC
        """
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                df["Træningspas"] = [f"Træningspas {i + 1}" for i in range(len(df))]
            return df

    def read_sets_for_session(self, session_date: str) -> pd.DataFrame:
        """Henter de enkelte løft for et specifikt træningspas baseret på dato."""
        query = """
            SELECT s.id, s.ovelse AS "Øvelse", s.vaegt AS "Vægt (kg)", 
                   s.reps AS "Reps", s.estimeret_1rm AS "Estimeret 1RM (kg)", 
                   s.noter AS "Noter"
            FROM workout_sets s
            JOIN workout_sessions w ON s.session_id = w.id
            WHERE w.dato = ?
            ORDER BY s.id ASC
        """
        with self._get_connection() as conn:
            return pd.read_sql_query(query, conn, params=(session_date,))

    def add_training_entry(self, dato: str, ovelse: str, vaegt: float, reps: int, est_1rm: float, noter: str = "") -> None:
        """Tilføjer et løft. Opretter automatisk træningspasset, hvis datoen ikke findes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM workout_sessions WHERE dato = ?", (dato,))
            row = cursor.fetchone()
            if row:
                session_id = row[0]
            else:
                cursor.execute("INSERT INTO workout_sessions (dato) VALUES (?)", (dato,))
                session_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, ovelse, vaegt, reps, est_1rm, noter))
            conn.commit()

    def update_training_set(self, set_id: int, ovelse: str, vaegt: float, reps: int, est_1rm: float, noter: str) -> None:
        """Opdaterer et eksisterende sæt i databasen."""
        query = """
            UPDATE workout_sets 
            SET ovelse = ?, vaegt = ?, reps = ?, estimeret_1rm = ?, noter = ?
            WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (ovelse, vaegt, reps, est_1rm, noter, set_id))
            conn.commit()

    def delete_workout_session_by_date(self, dato: str) -> None:
        """Sletter hele træningspasset og alle dets tilhørende sæt."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM workout_sessions WHERE dato = ?", (dato,))
            conn.commit()

    # --- Kropsvægt ---
    def read_bodyweight_log(self) -> pd.DataFrame:
        query = """
            SELECT id, dato AS "Dato", vaegt AS "Kropsvægt (kg)"
            FROM bodyweight_log
            ORDER BY dato ASC, id ASC
        """
        with self._get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def add_bodyweight_entry(self, dato: str, vaegt: float) -> None:
        with self._get_connection() as conn:
            conn.execute("INSERT INTO bodyweight_log (dato, vaegt) VALUES (?, ?)", (dato, vaegt))
            conn.commit()

    def delete_bodyweight_entry_by_id(self, entry_id: int) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM bodyweight_log WHERE id = ?", (entry_id,))
            conn.commit()