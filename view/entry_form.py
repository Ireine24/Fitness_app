from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QLabel, QComboBox, 
    QDateEdit, QDoubleSpinBox, QSpinBox, QPushButton, QSizePolicy
)
from PyQt6.QtCore import QDate
from model.workout_program import WORKOUT_PROGRAMS


class EntryFormWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Tilføj nyt løft", parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(8)

        def add_field(label_text: str, widget, width: int = None):
            pair_layout = QHBoxLayout()
            pair_layout.setSpacing(4)
            pair_layout.addWidget(QLabel(label_text))
            if width:
                widget.setFixedWidth(width)
                widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            pair_layout.addWidget(widget)
            layout.addLayout(pair_layout)

        # 1. Dato
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        add_field("Dato:", self.input_date, width=105)

        # 2. Program (fast lille bredde)
        self.input_program = QComboBox()
        self.input_program.addItems(list(WORKOUT_PROGRAMS.keys()))
        self.input_program.currentIndexChanged.connect(self._on_program_changed)
        add_field("Prog:", self.input_program, width=70)

        # 3. Træning
        self.input_dag = QComboBox()
        self.input_dag.currentIndexChanged.connect(self._update_exercise_list)
        add_field("Træning:", self.input_dag, width=150)

        # 4. Øvelse
        self.input_ovelse = QComboBox()
        self.input_ovelse.setEditable(True)
        add_field("Øvelse:", self.input_ovelse, width=300)

        # Initialiser listerne ud fra første program
        self._on_program_changed()

        # 5. Vægt
        self.input_weight = QDoubleSpinBox()
        self.input_weight.setRange(0, 500)
        self.input_weight.setSingleStep(2.5)
        self.input_weight.setValue(80.0)
        add_field("Vægt (kg):", self.input_weight, width=90)

        # 6. Reps
        self.input_reps = QSpinBox()
        self.input_reps.setRange(1, 100)
        self.input_reps.setValue(5)
        add_field("Reps:", self.input_reps, width=75)

        # 7. Knap
        self.btn_add = QPushButton("Gem løft")
        self.btn_add.setFixedWidth(85)
        self.btn_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_add.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold; padding: 5px; border-radius: 4px;")
        layout.addWidget(self.btn_add)

        layout.addStretch()

    def _get_current_program_dict(self) -> dict:
        prog_name = self.input_program.currentText()
        return WORKOUT_PROGRAMS.get(prog_name, {})

    def _on_program_changed(self):
        self.input_dag.blockSignals(True)
        self.input_dag.clear()
        self.input_dag.addItem("Alle dage / øvelser")
        program_dict = self._get_current_program_dict()
        for dag, info in program_dict.items():
            self.input_dag.addItem(f"{dag} ({info['title']})")
        self.input_dag.blockSignals(False)
        self._update_exercise_list(0)

    def _populate_all_exercises(self):
        self.input_ovelse.clear()
        program_dict = self._get_current_program_dict()
        alle_program_ovelser = sorted({
            ex[0] for day in program_dict.values() for ex in day["exercises"]
        })
        self.input_ovelse.addItems(alle_program_ovelser)

    def _update_exercise_list(self, index: int):
        self.input_ovelse.clear()
        program_dict = self._get_current_program_dict()
        if index <= 0 or not program_dict:
            self._populate_all_exercises()
        else:
            dag_keys = list(program_dict.keys())
            if index - 1 < len(dag_keys):
                dag_key = dag_keys[index - 1]
                dag_ovelser = [ex[0] for ex in program_dict[dag_key]["exercises"]]
                self.input_ovelse.addItems(dag_ovelser)

    def get_data(self) -> dict:
        return {
            "dato": self.input_date.date().toString("yyyy-MM-dd"),
            "program": self.input_program.currentText().strip(),
            "traening": self.input_dag.currentText().strip(),
            "ovelse": self.input_ovelse.currentText().strip(),
            "vaegt": self.input_weight.value(),
            "reps": self.input_reps.value()
        }