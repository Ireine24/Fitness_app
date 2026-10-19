from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox


class TopBarWidget(QWidget):
    # Signal til at navigere til forside (indeks 0)
    go_home_signal = object() # Bruges via controller

    def __init__(self, default_file: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Tilbage til forside knap
        self.btn_home = QPushButton("🏠 Forside")
        self.btn_home.setStyleSheet("background-color: #333333; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;")
        layout.addWidget(self.btn_home)

        # Knap til at vælge fil
        self.btn_load = QPushButton("Vælg Database")
        layout.addWidget(self.btn_load)

        # Viser aktuel fil
        self.lbl_file = QLabel(f"Fil: {default_file}")
        layout.addWidget(self.lbl_file)

        # Vælg øvelse dropdown
        layout.addSpacing(20)
        layout.addWidget(QLabel("Vælg øvelse:"))
        self.combo_ovelse = QComboBox()
        self.combo_ovelse.addItem("Alle øvelser")
        layout.addWidget(self.combo_ovelse)

        layout.addStretch()

    def set_file_name(self, path: str):
        filename = path.split("/")[-1].split("\\")[-1]
        self.lbl_file.setText(f"Fil: {filename}")

    def update_exercises(self, exercises: list[str]):
        current = self.combo_ovelse.currentText()
        self.combo_ovelse.blockSignals(True)
        self.combo_ovelse.clear()
        self.combo_ovelse.addItem("Alle øvelser")
        for ex in exercises:
            self.combo_ovelse.addItem(ex)
        
        idx = self.combo_ovelse.findText(current)
        if idx >= 0:
            self.combo_ovelse.setCurrentIndex(idx)
        self.combo_ovelse.blockSignals(False)

    def get_selected_exercise(self) -> str:
        return self.combo_ovelse.currentText()