from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class HomeWidget(QWidget):
    # Signal der fortæller hovedvinduet, hvilken fane der skal skiftes til (indeks 1 til 4)
    navigate_to_tab = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # Velkomsttitel
        lbl_title = QLabel("Velkommen til Styrketræning Tracker")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 20px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_subtitle = QLabel("Vælg en funktion nedenfor for at komme i gang:")
        lbl_subtitle.setStyleSheet("font-size: 14px; color: #b0b0b0; margin-bottom: 30px;")
        lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_subtitle)

        # Grid med store "vinduer"/knapper
        grid = QGridLayout()
        grid.setSpacing(20)

        btn_graph = self._create_card("Styrkeudvikling (Graf)", "Se grafer over din styrkeudvikling og 1RM", "#2E7D32")
        btn_graph.clicked.connect(lambda: self.navigate_to_tab.emit(1))
        grid.addWidget(btn_graph, 0, 0)

        btn_table = self._create_card("Træningsoversigt (Pas & Løft)", "Se tidligere træningspas, sæt og rediger løft", "#1565C0")
        btn_table.clicked.connect(lambda: self.navigate_to_tab.emit(2))
        grid.addWidget(btn_table, 0, 1)

        btn_bw = self._create_card("Kropsvægt", "Registrer og følg din kropsvægt over tid", "#6A1B9A")
        btn_bw.clicked.connect(lambda: self.navigate_to_tab.emit(3))
        grid.addWidget(btn_bw, 1, 0)

        btn_prog = self._create_card("Træningsprogram", "Se dit ugentlige træningsprogram", "#E65100")
        btn_prog.clicked.connect(lambda: self.navigate_to_tab.emit(4))
        grid.addWidget(btn_prog, 1, 1)

        layout.addLayout(grid)

    def _create_card(self, title: str, description: str, bg_color: str) -> QPushButton:
        btn = QPushButton(f"{title}\n\n{description}")
        btn.setFixedSize(280, 140)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
                text-align: center;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: lighter({bg_color});
                border: 2px solid white;
            }}
        """)
        return btn