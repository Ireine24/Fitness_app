from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from model.workout_program import WORKOUT_PROGRAM


class ProgramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ScrollArea så programmet kan navigeres selv på mindre skærme
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        container = QWidget()
        cards_layout = QHBoxLayout(container)
        cards_layout.setSpacing(14)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for day, info in WORKOUT_PROGRAM.items():
            card = self._create_day_card(day, info)
            cards_layout.addWidget(card)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

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

        # Split (Push/Pull/Ben)
        lbl_title = QLabel(info["title"])
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Ekstra bemærkning (+ Mavetræning)
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