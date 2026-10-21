from __future__ import annotations
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDateEdit, QDoubleSpinBox, QSpinBox, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QAbstractItemView, QGroupBox
)
from PyQt6.QtCore import QDate


class RunningWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        form_box = QGroupBox("Registrer Løb")
        form_layout = QHBoxLayout(form_box)
        form_layout.setSpacing(10)

        def add_field(label: str, widget, width: int = None):
            pl = QHBoxLayout()
            pl.addWidget(QLabel(label))
            if width:
                widget.setFixedWidth(width)
            pl.addWidget(widget)
            form_layout.addLayout(pl)

        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        add_field("Dato:", self.input_date, 105)

        self.input_dist = QDoubleSpinBox()
        self.input_dist.setRange(0, 100)
        self.input_dist.setSingleStep(0.5)
        self.input_dist.setValue(5.0)
        add_field("Distance (km):", self.input_dist, 75)

        self.input_tid = QLineEdit()
        self.input_tid.setPlaceholderText("f.eks. 25:30")
        add_field("Tid:", self.input_tid, 85)

        self.input_pace = QLineEdit()
        self.input_pace.setPlaceholderText("f.eks. 5:05 /km")
        add_field("Pace:", self.input_pace, 95)

        self.input_noter = QLineEdit()
        self.input_noter.setPlaceholderText("Noter...")
        add_field("Noter:", self.input_noter, 140)

        self.btn_save = QPushButton("Gem løb")
        self.btn_save.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold; padding: 5px 10px; border-radius: 4px;")
        form_layout.addWidget(self.btn_save)
        form_layout.addStretch()
        layout.addWidget(form_box)

        table_box = QWidget()
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tb_layout.addWidget(self.table)

        self.btn_delete = QPushButton("Slet valgt løb")
        self.btn_delete.setStyleSheet("background-color: #7a1f1d; color: white; padding: 5px; font-weight: bold; border-radius: 4px;")
        tb_layout.addWidget(self.btn_delete)
        layout.addWidget(table_box, stretch=1)

    def get_input(self) -> tuple[str, float, str, str, str]:
        return (
            self.input_date.date().toString("yyyy-MM-dd"),
            self.input_dist.value(),
            self.input_tid.text().strip(),
            self.input_pace.text().strip(),
            self.input_noter.text().strip()
        )

    def get_selected_row(self) -> int:
        selected = self.table.selectionModel().selectedRows()
        return selected[0].row() if selected else -1

    def populate_table(self, df: pd.DataFrame | None):
        self.table.clear()
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        cols = ["Dato", "Distance (km)", "Tid", "Pace", "Noter"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(df))

        for row_idx, (_, row) in enumerate(df.iterrows()):
            d_val = row["Dato"]
            d_str = d_val.strftime("%Y-%m-%d") if isinstance(d_val, pd.Timestamp) else str(d_val)
            self.table.setItem(row_idx, 0, QTableWidgetItem(d_str))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{float(row['Distance (km)']):.1f} km"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row["Tid"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["Pace"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["Noter"])))


class SwimmingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        form_box = QGroupBox("Registrer Svømning")
        form_layout = QHBoxLayout(form_box)
        form_layout.setSpacing(10)

        def add_field(label: str, widget, width: int = None):
            pl = QHBoxLayout()
            pl.addWidget(QLabel(label))
            if width:
                widget.setFixedWidth(width)
            pl.addWidget(widget)
            form_layout.addLayout(pl)

        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        add_field("Dato:", self.input_date, 105)

        self.input_dist = QSpinBox()
        self.input_dist.setRange(0, 10000)
        self.input_dist.setSingleStep(100)
        self.input_dist.setValue(1500)
        add_field("Distance (m):", self.input_dist, 80)

        self.input_tid = QLineEdit()
        self.input_tid.setPlaceholderText("f.eks. 35:00")
        add_field("Tid:", self.input_tid, 85)

        self.input_fokus = QLineEdit()
        self.input_fokus.setPlaceholderText("f.eks. 4x50m benspark...")
        add_field("Fokus / Øvelser:", self.input_fokus, 150)

        self.input_noter = QLineEdit()
        self.input_noter.setPlaceholderText("Noter...")
        add_field("Noter:", self.input_noter, 130)

        self.btn_save = QPushButton("Gem svømning")
        self.btn_save.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold; padding: 5px 10px; border-radius: 4px;")
        form_layout.addWidget(self.btn_save)
        form_layout.addStretch()
        layout.addWidget(form_box)

        table_box = QWidget()
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tb_layout.addWidget(self.table)

        self.btn_delete = QPushButton("Slet valgt svømning")
        self.btn_delete.setStyleSheet("background-color: #7a1f1d; color: white; padding: 5px; font-weight: bold; border-radius: 4px;")
        tb_layout.addWidget(self.btn_delete)
        layout.addWidget(table_box, stretch=1)

    def get_input(self) -> tuple[str, int, str, str, str]:
        return (
            self.input_date.date().toString("yyyy-MM-dd"),
            self.input_dist.value(),
            self.input_tid.text().strip(),
            self.input_fokus.text().strip(),
            self.input_noter.text().strip()
        )

    def get_selected_row(self) -> int:
        selected = self.table.selectionModel().selectedRows()
        return selected[0].row() if selected else -1

    def populate_table(self, df: pd.DataFrame | None):
        self.table.clear()
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        cols = ["Dato", "Distance (m)", "Tid", "Fokus / Øvelser", "Noter"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(df))

        for row_idx, (_, row) in enumerate(df.iterrows()):
            d_val = row["Dato"]
            d_str = d_val.strftime("%Y-%m-%d") if isinstance(d_val, pd.Timestamp) else str(d_val)
            self.table.setItem(row_idx, 0, QTableWidgetItem(d_str))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{int(row['Distance (m)']):d} m"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row["Tid"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["Fokus / Øvelser"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["Noter"])))