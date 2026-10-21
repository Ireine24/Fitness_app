import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QDialog

from model.fitness_model import FitnessModel
from view.main_window import MainWindow
from view.user_dialog import UserSelectionDialog
from controller.main_controller import MainController


def main():
    app = QApplication(sys.argv)

    # Opret 'users' mappe og kopier eksisterende fitness.db derind første gang
    users_dir = "users"
    os.makedirs(users_dir, exist_ok=True)
    if os.path.exists("fitness.db") and not os.listdir(users_dir):
        shutil.copy("fitness.db", os.path.join(users_dir, "Standard.db"))

    # Vis brugervalg FØR hovedvinduet åbnes
    user_dialog = UserSelectionDialog(users_dir=users_dir)
    if user_dialog.exec() != QDialog.DialogCode.Accepted or not user_dialog.selected_db_path:
        sys.exit(0)  # Luk programmet hvis brugeren lukker dialogen uden at vælge

    db_path = user_dialog.selected_db_path
    model = FitnessModel(db_path=db_path)
    view = MainWindow(default_file=db_path)
    controller = MainController(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()