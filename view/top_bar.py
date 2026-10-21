from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class TopBarWidget(QWidget):
    def __init__(self, default_file: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Tilbage til forside knap
        self.btn_home = QPushButton("🏠 Forside")
        self.btn_home.setStyleSheet("background-color: #333333; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;")
        layout.addWidget(self.btn_home)

        # Knap til at skifte bruger
        self.btn_switch_user = QPushButton("👤 Skift Bruger")
        self.btn_switch_user.setStyleSheet("background-color: #1565C0; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;")
        layout.addWidget(self.btn_switch_user)

        # Knap til at vælge fil manuelt
        self.btn_load = QPushButton("Vælg Database")
        layout.addWidget(self.btn_load)

        # Viser aktuel bruger
        initial_user = default_file.split("/")[-1].split("\\")[-1].replace(".db", "")
        self.lbl_file = QLabel(f"Bruger: {initial_user}")
        self.lbl_file.setStyleSheet("font-weight: bold; color: #4CAF50; margin-left: 8px; font-size: 13px;")
        layout.addWidget(self.lbl_file)

        layout.addStretch()

    def set_file_name(self, path: str):
        username = path.split("/")[-1].split("\\")[-1].replace(".db", "")
        self.lbl_file.setText(f"Bruger: {username}")