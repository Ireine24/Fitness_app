from __future__ import annotations
import pandas as pd
from model.db_handler import DatabaseHandler
from model.calculations import calculate_epley_1rm


class FitnessModel:
    def __init__(self, db_path: str = "fitness.db"):
        self.file_path = db_path
        self.db_handler = DatabaseHandler(db_path)
        self.df: pd.DataFrame | None = None
        self.df_bodyweight: pd.DataFrame | None = None

    def set_file_path(self, path: str):
        self.file_path = path
        self.db_handler = DatabaseHandler(path)

    def load_data(self):
        self.df = self.db_handler.read_all_sets()
        if not self.df.empty:
            self.df["Dato"] = pd.to_datetime(self.df["Dato"])
            self.df["Estimeret_1RM"] = self.df["Vægt (kg)"] * (1 + self.df["Reps"] / 30.0)

        self.df_bodyweight = self.db_handler.read_bodyweight_log()
        if not self.df_bodyweight.empty:
            self.df_bodyweight["Dato"] = pd.to_datetime(self.df_bodyweight["Dato"])

    def get_exercises(self) -> list[str]:
        if self.df is None or self.df.empty:
            return []
        return sorted(self.df["Øvelse"].dropna().unique().tolist())

    def get_aggregated_plot_data(self, exercise: str = "Alle øvelser") -> pd.DataFrame | None:
        if self.df is None or self.df.empty:
            return None

        if exercise == "Alle øvelser" or not exercise:
            data = self.df
        else:
            data = self.df[self.df["Øvelse"] == exercise]

        return (
            data.groupby(["Dato", "Øvelse"], as_index=False)["Estimeret_1RM"]
            .max()
        )

    def get_workout_sessions(self) -> pd.DataFrame:
        return self.db_handler.read_workout_sessions_summary()

    def get_session_details(self, session_date: str) -> pd.DataFrame:
        return self.db_handler.read_sets_for_session(session_date)

    def add_entry(self, dato: str, ovelse: str, vaegt: float, reps: int):
        est_1rm = calculate_epley_1rm(vaegt, reps)
        self.db_handler.add_training_entry(dato, ovelse, vaegt, reps, est_1rm)

    def update_set_by_index(self, session_date: str, row_idx: int, ovelse: str, vaegt: float, reps: int, noter: str):
        """Opdaterer et specifikt sæt baseret på den valgte række i detaljetabellen."""
        details_df = self.get_session_details(session_date)
        if details_df is None or row_idx < 0 or row_idx >= len(details_df):
            return
        
        set_id = int(details_df.iloc[row_idx]["id"])
        est_1rm = calculate_epley_1rm(vaegt, reps)
        self.db_handler.update_training_set(set_id, ovelse, vaegt, reps, est_1rm, noter)

    def delete_workout_session(self, dato: str):
        self.db_handler.delete_workout_session_by_date(dato)

    def add_bodyweight_entry(self, dato: str, vaegt: float):
        self.db_handler.add_bodyweight_entry(dato, vaegt)

    def delete_bodyweight_entry(self, row_idx: int):
        if self.df_bodyweight is None or row_idx < 0 or row_idx >= len(self.df_bodyweight):
            return
        entry_id = int(self.df_bodyweight.iloc[row_idx]["id"])
        self.db_handler.delete_bodyweight_entry_by_id(entry_id)