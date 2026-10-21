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
        """Opretter tabellerne hvis de ikke findes, og sikrer at nye kolonner tilføjes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Træningspas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workout_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dato TEXT NOT NULL UNIQUE,
                    program TEXT DEFAULT '',
                    traening TEXT DEFAULT '',
                    noter TEXT DEFAULT ''
                )
            """)

            # Sikr at eksisterende databaser har program og traening kolonnerne
            cursor.execute("PRAGMA table_info(workout_sessions)")
            existing_cols = [col[1] for col in cursor.fetchall()]
            if "program" not in existing_cols:
                cursor.execute("ALTER TABLE workout_sessions ADD COLUMN program TEXT DEFAULT ''")
            if "traening" not in existing_cols:
                cursor.execute("ALTER TABLE workout_sessions ADD COLUMN traening TEXT DEFAULT ''")

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
        query = """
            SELECT 
                w.id AS session_id,
                w.dato AS "Dato",
                COALESCE(w.program, '') AS "Program",
                COALESCE(w.traening, '') AS "Træning",
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

    def add_training_entry(
        self, dato: str, ovelse: str, vaegt: float, reps: int, est_1rm: float, 
        program: str = "", traening: str = "", noter: str = ""
    ) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, program, traening FROM workout_sessions WHERE dato = ?", (dato,))
            row = cursor.fetchone()
            if row:
                session_id, existing_prog, existing_tr = row
                new_prog = program if program else (existing_prog or "")
                new_tr = traening if (traening and traening != "Alle dage / øvelser") else (existing_tr or "")
                cursor.execute(
                    "UPDATE workout_sessions SET program = ?, traening = ? WHERE id = ?",
                    (new_prog, new_tr, session_id)
                )
            else:
                clean_tr = traening if traening != "Alle dage / øvelser" else ""
                cursor.execute(
                    "INSERT INTO workout_sessions (dato, program, traening) VALUES (?, ?, ?)",
                    (dato, program, clean_tr)
                )
                session_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, ovelse, vaegt, reps, est_1rm, noter))
            conn.commit()

    def update_session_metadata(self, dato: str, program: str, traening: str) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE workout_sessions SET program = ?, traening = ? WHERE dato = ?",
                (program, traening, dato)
            )
            conn.commit()

    def update_training_set(self, set_id: int, ovelse: str, vaegt: float, reps: int, est_1rm: float, noter: str) -> None:
        query = """
            UPDATE workout_sets 
            SET ovelse = ?, vaegt = ?, reps = ?, estimeret_1rm = ?, noter = ?
            WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (ovelse, vaegt, reps, est_1rm, noter, set_id))
            conn.commit()

    def delete_workout_session_by_date(self, dato: str) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM workout_sessions WHERE dato = ?", (dato,))
            conn.commit()

    def delete_training_set_by_id(self, set_id: int) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM workout_sets WHERE id = ?", (set_id,))
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