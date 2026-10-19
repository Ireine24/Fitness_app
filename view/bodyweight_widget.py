from __future__ import annotations
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QDateEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QAbstractItemView, QGroupBox
)
from PyQt6.QtCore import QDate
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class BodyweightWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # 1. Indtastning i toppen
        form_box = QGroupBox("Registrer kropsvægt")
        form_layout = QHBoxLayout(form_box)
        form_layout.setSpacing(14)

        form_layout.addWidget(QLabel("Dato:"))
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        self.input_date.setMinimumWidth(110)
        form_layout.addWidget(self.input_date)

        form_layout.addWidget(QLabel("Kropsvægt (kg):"))
        self.input_bw = QDoubleSpinBox()
        self.input_bw.setRange(30.0, 250.0)
        self.input_bw.setSingleStep(0.1)
        self.input_bw.setDecimals(1)
        self.input_bw.setValue(85.0)
        self.input_bw.setMinimumWidth(100)
        form_layout.addWidget(self.input_bw)

        self.btn_save = QPushButton("Gem kropsvægt")
        self.btn_save.setMinimumWidth(130)
        form_layout.addWidget(self.btn_save)

        form_layout.addStretch()
        layout.addWidget(form_box)

        # 2. Split: Graf og Tabel side om side
        content_layout = QHBoxLayout()

        # Graf
        graph_box = QWidget()
        graph_layout = QVBoxLayout(graph_box)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        content_layout.addWidget(graph_box, stretch=3)

        # Tabel & slet
        table_box = QWidget()
        table_layout = QVBoxLayout(table_box)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        self.btn_delete = QPushButton("Slet valgt måling")
        self.btn_delete.setStyleSheet("background-color: #7a1f1d; color: white; padding: 5px;")
        table_layout.addWidget(self.btn_delete)

        content_layout.addWidget(table_box, stretch=2)
        layout.addLayout(content_layout, stretch=1)

    def draw_data(self, df: pd.DataFrame | None):
        self.figure.clear()
        if df is not None and not df.empty:
            ax = self.figure.add_subplot(111)
            sorted_df = df.sort_values("Dato")
            ax.plot(sorted_df["Dato"], sorted_df["Kropsvægt (kg)"], marker="o", color="#e67e22", linewidth=2)
            ax.set_title("Kropsvægt over tid", fontsize=11, fontweight="bold")
            ax.set_ylabel("Kg")
            ax.grid(True, linestyle="--", alpha=0.5)
            self.figure.autofmt_xdate()
            self.figure.tight_layout()
        self.canvas.draw()

    def populate_table(self, df: pd.DataFrame | None):
        self.table.clear()
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        cols = ["Dato", "Kropsvægt (kg)"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(df))

        for row_idx, (_, row) in enumerate(df.iterrows()):
            d_val = row["Dato"]
            d_str = d_val.strftime("%Y-%m-%d") if isinstance(d_val, pd.Timestamp) else str(d_val)
            self.table.setItem(row_idx, 0, QTableWidgetItem(d_str))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{row['Kropsvægt (kg)']:.1f} kg"))

    def get_input(self) -> tuple[str, float]:
        return self.input_date.date().toString("yyyy-MM-dd"), self.input_bw.value()

    def get_selected_row(self) -> int:
        selected = self.table.selectionModel().selectedRows()
        return selected[0].row() if selected else -1