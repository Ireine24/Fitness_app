import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class UserSelectionDialog(QDialog):
    def __init__(self, users_dir: str = "users", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vælg Bruger - Styrketræning Tracker")
        self.setFixedSize(380, 420)
        self.users_dir = users_dir
        self.selected_db_path: str | None = None
        self.selected_username: str | None = None

        os.makedirs(self.users_dir, exist_ok=True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl_title = QLabel("Hvem træner i dag?")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4CAF50;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_sub = QLabel("Vælg en profil fra listen eller opret en ny:")
        lbl_sub.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_sub)

        # Liste over eksisterende brugere
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                font-size: 15px; 
                padding: 6px; 
                background-color: #2b2b2b; 
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
            }
            QListWidget::item { padding: 8px; }
            QListWidget::item:selected { background-color: #2E7D32; border-radius: 4px; }
        """)
        self.user_list.itemDoubleClicked.connect(self._on_select_clicked)
        layout.addWidget(self.user_list)

        # Opret ny bruger
        new_user_layout = QHBoxLayout()
        self.input_new_user = QLineEdit()
        self.input_new_user.setPlaceholderText("Navn på ny bruger...")
        self.input_new_user.setStyleSheet("padding: 6px; font-size: 13px;")
        new_user_layout.addWidget(self.input_new_user)

        self.btn_create = QPushButton("+ Opret")
        self.btn_create.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold; padding: 6px 12px; border-radius: 4px;")
        self.btn_create.clicked.connect(self._on_create_user)
        new_user_layout.addWidget(self.btn_create)
        layout.addLayout(new_user_layout)

        # Bekræft-knap
        self.btn_select = QPushButton("Fortsæt til Forside ➔")
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        self.btn_select.clicked.connect(self._on_select_clicked)
        layout.addWidget(self.btn_select)

        self._load_users()

    def _load_users(self):
        self.user_list.clear()
        files = [f for f in os.listdir(self.users_dir) if f.endswith(".db")]
        for f in sorted(files):
            username = os.path.splitext(f)[0]
            self.user_list.addItem(username)

        if self.user_list.count() > 0:
            self.user_list.setCurrentRow(0)

    def _on_create_user(self):
        name = self.input_new_user.text().strip()
        if not name:
            QMessageBox.warning(self, "Advarsel", "Indtast venligst et gyldigt navn.")
            return

        safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()
        if not safe_name:
            QMessageBox.warning(self, "Advarsel", "Navnet må kun indeholde bogstaver og tal.")
            return

        db_path = os.path.join(self.users_dir, f"{safe_name}.db")
        if os.path.exists(db_path):
            QMessageBox.warning(self, "Advarsel", "Denne bruger findes allerede!")
            return

        # Opret en tom databasefil til brugeren
        open(db_path, "a").close()
        self.input_new_user.clear()
        self._load_users()

        items = self.user_list.findItems(safe_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.user_list.setCurrentItem(items[0])

    def _on_select_clicked(self):
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Advarsel", "Vælg venligst en bruger eller opret en ny.")
            return

        self.selected_username = current_item.text()
        self.selected_db_path = os.path.join(self.users_dir, f"{self.selected_username}.db")
        self.accept()