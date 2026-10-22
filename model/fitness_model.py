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
        self.df_running: pd.DataFrame | None = None
        self.df_swimming: pd.DataFrame | None = None

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

        if hasattr(self.db_handler, "read_running_log"):
            self.df_running = self.db_handler.read_running_log()
            if not self.df_running.empty:
                self.df_running["Dato"] = pd.to_datetime(self.df_running["Dato"])

        if hasattr(self.db_handler, "read_swimming_log"):
            self.df_swimming = self.db_handler.read_swimming_log()
            if not self.df_swimming.empty:
                self.df_swimming["Dato"] = pd.to_datetime(self.df_swimming["Dato"])

    def get_exercises(self) -> list[str]:
        if self.df is None or self.df.empty:
            return []
        return sorted(self.df["Øvelse"].dropna().unique().tolist())

    def get_aggregated_plot_data(self, exercise: str = "Alle øvelser") -> pd.DataFrame | None:
        if self.df is None or self.df.empty:
            return None

        if exercise == "Alle øvelser" or not exercise:
            daily_weight = (
                self.df.groupby(["Dato", "Øvelse"], as_index=False)["Vægt (kg)"]
                .max()
                .sort_values("Dato")
            )

            pivot_weight = daily_weight.pivot(index="Dato", columns="Øvelse", values="Vægt (kg)")
            pivot_weight = pivot_weight.sort_index().ffill()

            kg_changes = pd.DataFrame(index=pivot_weight.index)
            latest_gains = {}
            for col in pivot_weight.columns:
                series = pivot_weight[col].dropna()
                if not series.empty:
                    first_val = series.iloc[0]
                    kg_changes[col] = pivot_weight[col] - first_val
                    latest_gains[col] = series.iloc[-1] - first_val

            overall_kg = kg_changes.sum(axis=1).reset_index()
            overall_kg.columns = ["Dato", "Værdi"]
            overall_kg["Øvelse"] = "Samlet fremgang (kg)"

            sorted_gains = sorted(latest_gains.items(), key=lambda x: x[1], reverse=True)
            top_str = ", ".join(
                f"{ex} ({'+' if val >= 0 else ''}{val:g}kg)" 
                for ex, val in sorted_gains[:3] if val != 0
            )
            overall_kg["Top_Bidrag"] = top_str
            return overall_kg
        else:
            data = self.df[self.df["Øvelse"] == exercise].copy()
            data = data.sort_values(["Dato", "Vægt (kg)", "Reps"], ascending=[True, False, False])
            best_sets = data.drop_duplicates(subset=["Dato"], keep="first").sort_values("Dato")
            best_sets = best_sets.rename(columns={"Vægt (kg)": "Værdi"})
            return best_sets[["Dato", "Øvelse", "Værdi", "Reps"]]

    def get_strength_table_data(self, exercise: str = "Alle øvelser") -> pd.DataFrame | None:
        """Returnerer en DataFrame skræddersyet til Tabel-visningen under Styrkeudvikling."""
        if self.df is None or self.df.empty:
            return None

        # Find bedste sæt pr. dato for hver øvelse
        sorted_df = self.df.sort_values(["Dato", "Vægt (kg)", "Reps"], ascending=[True, False, False])
        daily_best = sorted_df.drop_duplicates(subset=["Dato", "Øvelse"], keep="first").sort_values("Dato")

        if exercise == "Alle øvelser" or not exercise:
            rows = []
            for ov, grp in daily_best.groupby("Øvelse"):
                grp = grp.sort_values("Dato")
                first_row = grp.iloc[0]
                last_row = grp.iloc[-1]
                max_w = grp["Vægt (kg)"].max()

                start_w = float(first_row["Vægt (kg)"])
                start_r = int(first_row["Reps"])
                curr_w = float(last_row["Vægt (kg)"])
                curr_r = int(last_row["Reps"])

                diff_kg = curr_w - start_w
                diff_pct = ((curr_w - start_w) / start_w * 100.0) if start_w > 0 else 0.0

                rows.append({
                    "Øvelse": ov,
                    "Startdato": first_row["Dato"].strftime("%Y-%m-%d"),
                    "Start (Sæt)": f"{start_w:g} kg × {start_r}",
                    "Seneste dato": last_row["Dato"].strftime("%Y-%m-%d"),
                    "Nuværende (Sæt)": f"{curr_w:g} kg × {curr_r}",
                    "PR (Maks kg)": f"{max_w:g} kg",
                    "Ændring (kg)": diff_kg,
                    "Ændring (%)": diff_pct,
                    "Antal pas": len(grp)
                })

            res_df = pd.DataFrame(rows)
            if not res_df.empty:
                res_df = res_df.sort_values("Ændring (kg)", ascending=False).reset_index(drop=True)
            return res_df
        else:
            grp = daily_best[daily_best["Øvelse"] == exercise].sort_values("Dato").copy()
            if grp.empty:
                return None

            start_w = float(grp.iloc[0]["Vægt (kg)"])
            prev_w = start_w
            rows = []
            for _, row in grp.iterrows():
                w = float(row["Vægt (kg)"])
                r = int(row["Reps"])
                diff_start = w - start_w
                diff_prev = w - prev_w
                diff_pct = ((w - start_w) / start_w * 100.0) if start_w > 0 else 0.0
                prev_w = w

                rows.append({
                    "Dato": row["Dato"].strftime("%Y-%m-%d"),
                    "Øvelse": exercise,
                    "Vægt (kg)": f"{w:g} kg",
                    "Reps": str(r),
                    "Sæt": f"{w:g} kg × {r}",
                    "Ændring fra sidst": diff_prev,
                    "Ændring siden start (kg)": diff_start,
                    "Ændring siden start (%)": diff_pct
                })
            return pd.DataFrame(rows)

    def get_workout_sessions(self) -> pd.DataFrame:
        return self.db_handler.read_workout_sessions_summary()

    def get_session_details(self, session_date: str) -> pd.DataFrame:
        return self.db_handler.read_sets_for_session(session_date)

    def add_entry(self, dato: str, ovelse: str, vaegt: float, reps: int, program: str = "", traening: str = ""):
        est_1rm = calculate_epley_1rm(vaegt, reps)
        self.db_handler.add_training_entry(dato, ovelse, vaegt, reps, est_1rm, program=program, traening=traening)

    def update_session_info(self, dato: str, program: str, traening: str):
        self.db_handler.update_session_metadata(dato, program, traening)

    def update_set_by_index(self, session_date: str, row_idx: int, ovelse: str, vaegt: float, reps: int, noter: str):
        details_df = self.get_session_details(session_date)
        if details_df is None or row_idx < 0 or row_idx >= len(details_df):
            return
        
        set_id = int(details_df.iloc[row_idx]["id"])
        est_1rm = calculate_epley_1rm(vaegt, reps)
        self.db_handler.update_training_set(set_id, ovelse, vaegt, reps, est_1rm, noter)

    def delete_set_by_index(self, session_date: str, row_idx: int):
        details_df = self.get_session_details(session_date)
        if details_df is None or row_idx < 0 or row_idx >= len(details_df):
            return
        set_id = int(details_df.iloc[row_idx]["id"])
        self.db_handler.delete_training_set_by_id(set_id)

    def delete_workout_session(self, dato: str):
        self.db_handler.delete_workout_session_by_date(dato)

    def add_bodyweight_entry(self, dato: str, vaegt: float):
        self.db_handler.add_bodyweight_entry(dato, vaegt)

    def delete_bodyweight_entry(self, row_idx: int):
        if self.df_bodyweight is None or row_idx < 0 or row_idx >= len(self.df_bodyweight):
            return
        entry_id = int(self.df_bodyweight.iloc[row_idx]["id"])
        self.db_handler.delete_bodyweight_entry_by_id(entry_id)

    def add_running_entry(self, dato: str, dist_km: float, tid: str, pace: str, noter: str):
        self.db_handler.add_running_entry(dato, dist_km, tid, pace, noter)

    def delete_running_entry(self, row_idx: int):
        if self.df_running is None or row_idx < 0 or row_idx >= len(self.df_running):
            return
        entry_id = int(self.df_running.iloc[row_idx]["id"])
        self.db_handler.delete_running_entry_by_id(entry_id)

    def add_swimming_entry(self, dato: str, dist_meter: int, tid: str, fokus: str, noter: str):
        self.db_handler.add_swimming_entry(dato, dist_meter, tid, fokus, noter)

    def delete_swimming_entry(self, row_idx: int):
        if self.df_swimming is None or row_idx < 0 or row_idx >= len(self.df_swimming):
            return
        entry_id = int(self.df_swimming.iloc[row_idx]["id"])
        self.db_handler.delete_swimming_entry_by_id(entry_id)