from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog, 
    QMessageBox, QTabWidget
)
from view.top_bar import TopBarWidget
from view.plot_widget import PlotWidget
from view.table_widget import TableWidget
from view.cardio_widgets import RunningWidget, SwimmingWidget
from view.bodyweight_widget import BodyweightWidget
from view.program_widget import ProgramWidget
from view.home_widget import HomeWidget

class MainWindow(QMainWindow):
    def __init__(self, default_file: str):
        super().__init__()
        self.setWindowTitle("Styrketræning Tracker")
        self.resize(1150, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.top_bar = TopBarWidget(default_file)

        self.tabs = QTabWidget()
        self.home_widget = HomeWidget()
        self.plot_widget = PlotWidget()
        self.table_widget = TableWidget()
        self.running_widget = RunningWidget()
        self.swimming_widget = SwimmingWidget()
        self.bw_widget = BodyweightWidget()
        self.program_widget = ProgramWidget()

        self.entry_form = self.table_widget.entry_form

        # Rækkefølgen her bestemmer indeks (0 til 6)
        self.tabs.addTab(self.home_widget, "Forside")
        self.tabs.addTab(self.plot_widget, "Styrkeudvikling (Graf)")
        self.tabs.addTab(self.table_widget, "Træningsoversigt (Pas && Løft)")
        self.tabs.addTab(self.running_widget, "Løb")
        self.tabs.addTab(self.swimming_widget, "Svømning")
        self.tabs.addTab(self.bw_widget, "Kropsvægt")
        self.tabs.addTab(self.program_widget, "Træningsprogram")

        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.tabs, stretch=1)

    def prompt_file_selection(self) -> str:
        fil, _ = QFileDialog.getOpenFileName(
            self, "Vælg databasefil", "", "SQLite Database (*.db *.sqlite *.db3)"
        )
        return fil

    def show_info(self, title: str, text: str):
        QMessageBox.information(self, title, text)

    def show_warning(self, title: str, text: str):
        QMessageBox.warning(self, title, text)

    def show_error(self, title: str, text: str):
        QMessageBox.critical(self, title, text)

    def ask_confirmation(self, title: str, text: str) -> bool:
        reply = QMessageBox.question(
            self, title, text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes