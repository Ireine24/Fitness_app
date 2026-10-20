from __future__ import annotations
from model.db_handler import DatabaseHandler

class FitnessModel:
    def __init__(self, db_path: str = "fitness.db"):
        self.file_path = db_path
        self.db_handler = DatabaseHandler(db_path)

    def load_data(self):
        # Indlæsningslogik hvis nødvendigt
        pass

    def get_program_for_day(self, day_name: str) -> list:
        """Henter øvelser og sæt for en given ugedag via DatabaseHandler."""
        return self.db_handler.get_program_for_day(day_name)

    