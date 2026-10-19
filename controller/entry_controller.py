from model.fitness_model import FitnessModel
from view.main_window import MainWindow


class EntryController:
    def __init__(self, model: FitnessModel, view: MainWindow):
        self.model = model
        self.view = view

    def handle_add_entry(self) -> bool:
        data = self.view.entry_form.get_data()

        if not data["ovelse"]:
            self.view.show_warning("Advarsel", "Skriv eller vælg venligst en øvelse.")
            return False

        try:
            self.model.add_entry(
                dato=data["dato"],
                ovelse=data["ovelse"],
                vaegt=data["vaegt"],
                reps=data["reps"]
            )
            self.view.show_info("Succes", "Nyt pas blev gemt i Excel!")
            return True
        except PermissionError:
            self.view.show_error("Fejl", "Luk venligst Excel-programmet, da filen er låst.")
        except FileNotFoundError as e:
            self.view.show_warning("Advarsel", str(e))
        except Exception as e:
            self.view.show_error("Fejl", f"Kunne ikke gemme:\n{e}")

        return False