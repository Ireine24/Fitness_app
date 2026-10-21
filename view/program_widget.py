from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from model.workout_program import WORKOUT_PROGRAMS


class ProgramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Top-sektion med valg af program
        top_layout = QHBoxLayout()
        lbl_select = QLabel("Vælg træningsprogram:")
        lbl_select.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50;")
        top_layout.addWidget(lbl_select)

        self.combo_program = QComboBox()
        self.combo_program.addItems(list(WORKOUT_PROGRAMS.keys()))
        self.combo_program.setMinimumWidth(250)
        self.combo_program.currentIndexChanged.connect(self._on_program_changed)
        top_layout.addWidget(self.combo_program)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # 2. ScrollArea til dag-kortene
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.container = QWidget()
        self.cards_layout = QHBoxLayout(self.container)
        self.cards_layout.setSpacing(14)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.container)
        main_layout.addWidget(scroll)

        # Indlæs standardprogrammet ved opstart
        self._load_program(list(WORKOUT_PROGRAMS.keys())[0])

    def _on_program_changed(self, index: int):
        program_name = self.combo_program.itemText(index)
        self._load_program(program_name)

    def _load_program(self, program_name: str):
        # Ryd eksisterende kort
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Tilføj nye kort baseret på det valgte program
        program_data = WORKOUT_PROGRAMS[program_name]
        for day, info in program_data.items():
            card = self._create_day_card(day, info)
            self.cards_layout.addWidget(card)

    def _create_day_card(self, day: str, info: dict) -> QFrame:
        card = QFrame()
        card.setFixedWidth(220)
        card.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Ugedag
        lbl_day = QLabel(day)
        lbl_day.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_day)

        # Titel (F.eks. Push 1 eller Overkrop)
        lbl_title = QLabel(info["title"])
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Ekstra bemærkning
        if info["extra"]:
            lbl_extra = QLabel(info["extra"])
            lbl_extra.setStyleSheet("font-size: 11px; font-weight: bold; color: #ff4081;")
            lbl_extra.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_extra)

        # Skillelinje
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #4a4a4a;")
        layout.addWidget(line)

        # Øvelser og sæt/reps
        for ex_name, reps in info["exercises"]:
            ex_box = QVBoxLayout()
            ex_box.setSpacing(1)

            lbl_name = QLabel(ex_name)
            lbl_name.setWordWrap(True)
            lbl_name.setStyleSheet("font-weight: 500; font-size: 12px; color: #e0e0e0;")

            lbl_reps = QLabel(reps)
            lbl_reps.setStyleSheet("color: #ff5252; font-size: 11px; font-weight: bold;")

            ex_box.addWidget(lbl_name)
            ex_box.addWidget(lbl_reps)
            layout.addLayout(ex_box)
            layout.addSpacing(4)

        layout.addStretch()
        return card