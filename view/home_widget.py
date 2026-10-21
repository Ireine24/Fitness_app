from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os


class HomeWidget(QWidget):
    navigate_to_tab = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel("Velkommen til Styrketræning Tracker")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 10px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(lbl_title)

        lbl_subtitle = QLabel("Vælg en funktion nedenfor for at komme i gang:")
        lbl_subtitle.setStyleSheet("font-size: 14px; color: #b0b0b0; margin-bottom: 25px;")
        lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(lbl_subtitle)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_graph = self._create_card("Styrkeudvikling (Graf)", "Se grafer over din\nstyrkeudvikling og 1RM", "#2E7D32")
        btn_graph.clicked.connect(lambda: self.navigate_to_tab.emit(1))
        grid.addWidget(btn_graph, 0, 0)

        btn_table = self._create_card("Træningsoversigt (Pas && Løft)", "Se tidligere træningspas,\nsæt og rediger løft", "#1565C0")
        btn_table.clicked.connect(lambda: self.navigate_to_tab.emit(2))
        grid.addWidget(btn_table, 0, 1)

        btn_run = self._create_card("Løb", "Log løbeture,\ndistance og pace", "#00897B")
        btn_run.clicked.connect(lambda: self.navigate_to_tab.emit(3))
        grid.addWidget(btn_run, 1, 0)

        btn_swim = self._create_card("Svømning", "Log svømmetræning,\nintervaller og fokus", "#0277BD")
        btn_swim.clicked.connect(lambda: self.navigate_to_tab.emit(4))
        grid.addWidget(btn_swim, 1, 1)

        btn_bw = self._create_card("Kropsvægt", "Registrer og følg din\nkropsvægt over tid", "#6A1B9A")
        btn_bw.clicked.connect(lambda: self.navigate_to_tab.emit(5))
        grid.addWidget(btn_bw, 2, 0)

        btn_prog = self._create_card("Træningsprogram", "Se dit ugentlige\ntræningsprogram", "#E65100")
        btn_prog.clicked.connect(lambda: self.navigate_to_tab.emit(6))
        grid.addWidget(btn_prog, 2, 1)

        left_layout.addLayout(grid)
        main_layout.addWidget(left_container, stretch=3)

        self.lbl_image = QLabel()
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pixmap = QPixmap()
        for filename in ["goku.jpg", "goku.png", "Goku.jpg", "Goku.png"]:
            if os.path.exists(filename):
                self.pixmap = QPixmap(filename)
                break

        main_layout.addWidget(self.lbl_image, stretch=1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.pixmap.isNull():
            target_height = self.height() - 60
            scaled_pixmap = self.pixmap.scaledToHeight(target_height, Qt.TransformationMode.SmoothTransformation)
            self.lbl_image.setPixmap(scaled_pixmap)

    def _create_card(self, title: str, description: str, bg_color: str) -> QPushButton:
        btn = QPushButton(f"{title}\n\n{description}")
        btn.setFixedSize(240, 110)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 10px;
                text-align: center;
                padding: 8px;
            }}
            QPushButton:hover {{
                border: 2px solid white;
            }}
        """)
        return btn