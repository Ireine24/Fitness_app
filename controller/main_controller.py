from PyQt6.QtWidgets import QDialog
from model.fitness_model import FitnessModel
from view.main_window import MainWindow
from view.user_dialog import UserSelectionDialog
from controller.plot_controller import PlotController
from controller.entry_controller import EntryController


class MainController:
    def __init__(self, model: FitnessModel, view: MainWindow):
        self.model = model
        self.view = view

        self.plot_controller = PlotController(self.model, self.view.plot_widget)
        self.entry_controller = EntryController(self.model, self.view)

        self._bind_signals()
        self.reload_data()

    def _bind_signals(self):
        # Gå til forsiden via topbar knap og forside-kort
        self.view.top_bar.btn_home.clicked.connect(lambda: self.view.tabs.setCurrentIndex(0))
        self.view.home_widget.navigate_to_tab.connect(self.view.tabs.setCurrentIndex)

        # Skift bruger eller databasefil
        self.view.top_bar.btn_switch_user.clicked.connect(self._on_switch_user)
        self.view.top_bar.btn_load.clicked.connect(self._on_select_file)

        # Træning og graf-filtrering (inde i plot_widget)
        self.view.plot_widget.combo_ovelse.currentIndexChanged.connect(self._on_exercise_changed)
        self.view.entry_form.btn_add.clicked.connect(self._on_add_entry)
        self.view.table_widget.btn_delete.clicked.connect(self._on_delete_entry)
        
        # Valg og redigering i tabeller
        self.view.table_widget.table_sessions.itemSelectionChanged.connect(self._on_session_selected)
        self.view.table_widget.session_meta_changed.connect(self._on_session_meta_changed)
        self.view.table_widget.set_item_changed.connect(self._on_set_edited)
        self.view.table_widget.delete_set_signal.connect(self._on_delete_set)

        # Kropsvægt
        self.view.bw_widget.btn_save.clicked.connect(self._on_save_bodyweight)
        self.view.bw_widget.btn_delete.clicked.connect(self._on_delete_bodyweight)

    def _on_switch_user(self):
        dialog = UserSelectionDialog(users_dir="users", parent=self.view)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_db_path:
            self.model.set_file_path(dialog.selected_db_path)
            self.view.top_bar.set_file_name(dialog.selected_db_path)
            self.reload_data()
            self.view.tabs.setCurrentIndex(0)

    def _on_session_selected(self):
        selected_date, session_navn = self.view.table_widget.get_selected_session_info()
        if selected_date:
            details_df = self.model.get_session_details(selected_date)
            self.view.table_widget.populate_session_details(details_df, selected_date, session_navn or "")

    def _on_session_meta_changed(self, dato: str, program: str, traening: str):
        self.model.update_session_info(dato, program, traening)
        self._on_session_selected()

    def _on_set_edited(self, row: int, col: int, new_value: str):
        selected_date, _ = self.view.table_widget.get_selected_session_info()
        if not selected_date:
            return

        details_df = self.model.get_session_details(selected_date)
        if details_df is None or row >= len(details_df):
            return

        row_data = details_df.iloc[row]
        ovelse = row_data["Øvelse"]
        vaegt = float(row_data["Vægt (kg)"])
        reps = int(row_data["Reps"])
        noter = str(row_data["Noter"])

        try:
            if col == 0:
                ovelse = new_value.strip()
            elif col == 1:
                vaegt = float(new_value.replace("kg", "").strip())
            elif col == 2:
                reps = int(new_value.strip())
            elif col == 4:
                noter = new_value.strip()

            self.model.update_set_by_index(selected_date, row, ovelse, vaegt, reps, noter)
            self.reload_data(keep_selection=selected_date)
        except ValueError:
            self.view.show_warning("Ugyldig indtastning", "Kontrollér at vægt og reps er angivet med korrekte talværdier.")

    def _on_delete_set(self, row: int):
        selected_date, _ = self.view.table_widget.get_selected_session_info()
        if not selected_date:
            return

        if not self.view.ask_confirmation("Bekræft sletning", "Vil du slette dette enkelte sæt/løft?"):
            return

        try:
            self.model.delete_set_by_index(selected_date, row)
            self.reload_data(keep_selection=selected_date)
            self.view.show_info("Succes", "Sættet blev slettet.")
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke slette sættet:\n{e}")

    def _on_select_file(self):
        new_path = self.view.prompt_file_selection()
        if new_path:
            self.model.set_file_path(new_path)
            self.view.top_bar.set_file_name(new_path)
            self.reload_data()

    def _on_exercise_changed(self):
        selected = self.view.plot_widget.get_selected_exercise()
        self.plot_controller.update_plot(selected)

    def _on_add_entry(self):
        data = self.view.entry_form.get_data()
        if self.entry_controller.handle_add_entry():
            self.reload_data(keep_selection=data["dato"])

    def _on_delete_entry(self):
        selected_date, session_navn = self.view.table_widget.get_selected_session_info()
        if not selected_date:
            self.view.show_warning("Advarsel", "Vælg venligst et træningspas i tabellen for at slette.")
            return

        navn_tekst = f"{session_navn} ({selected_date})" if session_navn else selected_date
        if not self.view.ask_confirmation("Bekræft sletning", f"Er du sikker på, at du vil slette {navn_tekst}?"):
            return

        try:
            self.model.delete_workout_session(selected_date)
            self.reload_data()
            self.view.show_info("Succes", f"{navn_tekst} blev slettet.")
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke slette:\n{e}")

    def _on_save_bodyweight(self):
        dato, vaegt = self.view.bw_widget.get_input()
        try:
            self.model.add_bodyweight_entry(dato, vaegt)
            self.reload_data()
            self.view.show_info("Succes", "Kropsvægt gemt!")
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke gemme kropsvægt:\n{e}")

    def _on_delete_bodyweight(self):
        row = self.view.bw_widget.get_selected_row()
        if row < 0:
            self.view.show_warning("Advarsel", "Vælg en måling i kropsvægtstabellen for at slette.")
            return

        if not self.view.ask_confirmation("Bekræft sletning", "Vil du slette denne kropsvægtmåling?"):
            return

        try:
            self.model.delete_bodyweight_entry(row)
            self.reload_data()
            self.view.show_info("Succes", "Måling slettet.")
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke slette:\n{e}")

    def reload_data(self, keep_selection: str | None = None):
        try:
            self.model.load_data()
            exercises = self.model.get_exercises()
            self.view.plot_widget.update_exercises(exercises)
            
            sessions = self.model.get_workout_sessions()
            self.view.table_widget.populate_sessions(sessions)

            if keep_selection and not sessions.empty:
                for r in range(self.view.table_widget.table_sessions.rowCount()):
                    item = self.view.table_widget.table_sessions.item(r, 0)
                    if item and item.text() == keep_selection:
                        self.view.table_widget.table_sessions.selectRow(r)
                        break

            self._on_session_selected()

            self.view.bw_widget.populate_table(self.model.df_bodyweight)
            self.view.bw_widget.draw_data(self.model.df_bodyweight)
            
            self._on_exercise_changed()
        except FileNotFoundError:
            pass
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke indlæse data:\n{e}")