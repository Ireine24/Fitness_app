import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView,
    QLabel, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal


class TableWidget(QWidget):
    # Signal der udløses når et sæt ændres: (row_idx, column_idx, new_value)
    set_item_changed = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        splitter = QSplitter(Qt.Orientation.Vertical)

        # --- 1. Øverste sektion: Oversigt over træningspas ---
        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_sessions = QLabel("Træningspas (Klik på et pas for at se alle løft):")
        lbl_sessions.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50;")
        top_layout.addWidget(lbl_sessions)

        self.table_sessions = QTableWidget()
        self.table_sessions.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_sessions.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_sessions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        top_layout.addWidget(self.table_sessions)

        splitter.addWidget(top_container)

        # --- 2. Nederste sektion: Enkelte løft (redigerbare) ---
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 6, 0, 0)

        self.lbl_details = QLabel("Enkelte løft for det valgte pas (klik i cellerne for at rette):")
        self.lbl_details.setStyleSheet("font-weight: bold; font-size: 13px; color: #64B5F6;")
        bottom_layout.addWidget(self.lbl_details)

        self.table_details = QTableWidget()
        self.table_details.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_details.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # Tillad redigering direkte i tabellen ved dobbeltklik/skrivning
        self.table_details.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed | QAbstractItemView.EditTrigger.SelectedClicked)
        bottom_layout.addWidget(self.table_details)

        # Forbind ændringer i celler
        self.table_details.cellChanged.connect(self._on_cell_changed)

        splitter.addWidget(bottom_container)
        layout.addWidget(splitter, stretch=1)

        # --- Knap til sletning ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_delete = QPushButton("Slet valgt træningspas")
        self.btn_delete.setStyleSheet("background-color: #7a1f1d; color: white; padding: 6px 14px; font-weight: bold; border-radius: 4px;")
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self._is_populating = False

    def _on_cell_changed(self, row: int, col: int):
        if self._is_populating:
            return
        item = self.table_details.item(row, col)
        if item:
            self.set_item_changed.emit(row, col, item.text())

    def populate_sessions(self, df_sessions: pd.DataFrame | None):
        """Udfylder den øverste oversigtstabel."""
        self.table_sessions.clear()
        if df_sessions is None or df_sessions.empty:
            self.table_sessions.setRowCount(0)
            self.table_sessions.setColumnCount(0)
            self.table_details.clear()
            self.table_details.setRowCount(0)
            return

        cols = ["Dato", "Træningspas", "Sæt", "Total volumen (kg)", "Maks 1RM (kg)"]
        self.table_sessions.setColumnCount(len(cols))
        self.table_sessions.setHorizontalHeaderLabels(cols)
        self.table_sessions.setRowCount(len(df_sessions))

        for row_idx, (_, row) in enumerate(df_sessions.iterrows()):
            self.table_sessions.setItem(row_idx, 0, QTableWidgetItem(str(row["Dato"])))
            self.table_sessions.setItem(row_idx, 1, QTableWidgetItem(str(row["Træningspas"])))
            self.table_sessions.setItem(row_idx, 2, QTableWidgetItem(str(row["Sæt"])))
            self.table_sessions.setItem(row_idx, 3, QTableWidgetItem(f"{float(row['Total volumen (kg)']):.1f} kg"))
            self.table_sessions.setItem(row_idx, 4, QTableWidgetItem(f"{float(row['Maks 1RM (kg)']):.1f} kg"))

        header = self.table_sessions.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        if len(df_sessions) > 0 and self.table_sessions.currentRow() < 0:
            self.table_sessions.selectRow(len(df_sessions) - 1)

    def populate_session_details(self, df_details: pd.DataFrame | None, dato_str: str, session_navn: str = ""):
        """Udfylder den nederste tabel med de enkelte sæt."""
        self._is_populating = True
        self.table_details.clear()
        titel = f"{session_navn} ({dato_str})" if session_navn else dato_str
        self.lbl_details.setText(f"Enkelte løft for {titel} (Klik på en celle for at redigere):")
        
        if df_details is None or df_details.empty:
            self.table_details.setRowCount(0)
            self.table_details.setColumnCount(0)
            self._is_populating = False
            return

        cols = ["Øvelse", "Vægt (kg)", "Reps", "Estimeret 1RM (kg)", "Noter"]
        self.table_details.setColumnCount(len(cols))
        self.table_details.setHorizontalHeaderLabels(cols)
        self.table_details.setRowCount(len(df_details))

        for row_idx, (_, row) in enumerate(df_details.iterrows()):
            self.table_details.setItem(row_idx, 0, QTableWidgetItem(str(row.get("Øvelse", ""))))
            
            # Rens vægt og reps for tekst-enheder ved visning
            w_val = float(row.get("Vægt (kg)", 0))
            self.table_details.setItem(row_idx, 1, QTableWidgetItem(str(w_val)))
            
            r_val = int(row.get("Reps", 0))
            self.table_details.setItem(row_idx, 2, QTableWidgetItem(str(r_val)))
            
            est_val = float(row.get("Estimeret 1RM (kg)", 0.0))
            item_1rm = QTableWidgetItem(f"{est_val:.1f}")
            item_1rm.setFlags(item_1rm.flags() & ~Qt.ItemFlag.ItemIsEditable) # 1RM kan ikke redigeres manuelt (beregnes)
            self.table_details.setItem(row_idx, 3, item_1rm)
            
            self.table_details.setItem(row_idx, 4, QTableWidgetItem(str(row.get("Noter", ""))))

        header = self.table_details.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        self._is_populating = False

    def get_selected_session_info(self) -> tuple[str | None, str | None]:
        selected_rows = self.table_sessions.selectionModel().selectedRows()
        if not selected_rows:
            return None, None
        row = selected_rows[0].row()
        item_date = self.table_sessions.item(row, 0)
        item_name = self.table_sessions.item(row, 1)
        dato = item_date.text() if item_date else None
        navn = item_name.text() if item_name else None
        return dato, navn