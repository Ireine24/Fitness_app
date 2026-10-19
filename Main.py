import sys
from PyQt6.QtWidgets import QApplication

from model.fitness_model import FitnessModel
from view.main_window import MainWindow
from controller.main_controller import MainController


def main():
    app = QApplication(sys.argv)

    default_file = "fitness.db"
    model = FitnessModel(db_path=default_file)
    view = MainWindow(default_file=default_file)
    controller = MainController(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()