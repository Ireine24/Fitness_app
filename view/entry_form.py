from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QLabel, QComboBox, 
    QDateEdit, QDoubleSpinBox, QSpinBox, QPushButton
)
from PyQt6.QtCore import QDate

# 1. Importér træningsprogrammet her i toppen
from model.workout_program import WORKOUT_PROGRAM


class EntryFormWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Tilføj nyt løft", parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(16)

        def add_field(label_text: str, widget, min_width: int = None):
            pair_layout = QHBoxLayout()
            pair_layout.setSpacing(6)
            pair_layout.addWidget(QLabel(label_text))
            if min_width:
                widget.setMinimumWidth(min_width)
            pair_layout.addWidget(widget)
            layout.addLayout(pair_layout)

        # 1. Dato
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        add_field("Dato:", self.input_date, min_width=120)

        # 2. Øvelse
        self.input_ovelse = QComboBox()
        self.input_ovelse.setEditable(True)

        # --- HER ER KODEN INDSAT ---
        alle_program_ovelser = sorted({
            ex[0] for day in WORKOUT_PROGRAM.values() for ex in day["exercises"]
        })
        self.input_ovelse.addItems(alle_program_ovelser)
        # ---------------------------

        add_field("Øvelse:", self.input_ovelse, min_width=180)

        # 3. Vægt
        self.input_weight = QDoubleSpinBox()
        self.input_weight.setRange(0, 500)
        self.input_weight.setSingleStep(2.5)
        self.input_weight.setValue(80.0)
        add_field("Vægt (kg):", self.input_weight, min_width=110)

        # 4. Reps
        self.input_reps = QSpinBox()
        self.input_reps.setRange(1, 100)
        self.input_reps.setValue(5)
        add_field("Reps:", self.input_reps, min_width=85)

        # 5. Knap
        self.btn_add = QPushButton("Gem i Excel")
        self.btn_add.setMinimumWidth(110)
        layout.addWidget(self.btn_add)

        layout.addStretch()

    def get_data(self) -> dict:
        return {
            "dato": self.input_date.date().toString("yyyy-MM-dd"),
            "ovelse": self.input_ovelse.currentText().strip(),
            "vaegt": self.input_weight.value(),
            "reps": self.input_reps.value()
        }