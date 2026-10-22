from __future__ import annotations
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Top-bar inde på fanen med valg af øvelse + skift mellem Graf og Tabel
        filter_layout = QHBoxLayout()
        lbl_filter = QLabel("Vælg øvelse:")
        lbl_filter.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50;")
        filter_layout.addWidget(lbl_filter)

        self.combo_ovelse = QComboBox()
        self.combo_ovelse.addItem("Alle øvelser")
        self.combo_ovelse.setMinimumWidth(220)
        filter_layout.addWidget(self.combo_ovelse)

        filter_layout.addSpacing(20)

        lbl_view = QLabel("Visning:")
        lbl_view.setStyleSheet("font-weight: bold; font-size: 13px; color: #b0b0b0;")
        filter_layout.addWidget(lbl_view)

        self.btn_show_graph = QPushButton("📈 Vis Graf")
        self.btn_show_table = QPushButton("📋 Vis Tabel")
        self.btn_show_graph.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_show_table.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_show_graph.clicked.connect(lambda: self._switch_view(0))
        self.btn_show_table.clicked.connect(lambda: self._switch_view(1))

        filter_layout.addWidget(self.btn_show_graph)
        filter_layout.addWidget(self.btn_show_table)
        filter_layout.addStretch()

        layout.addLayout(filter_layout)

        # StackedWidget så man kan skifte mellem Graf (side 0) og Tabel (side 1)
        self.stack = QStackedWidget()

        # --- SIDE 0: GRAF ---
        self.graph_page = QWidget()
        graph_layout = QVBoxLayout(self.graph_page)
        graph_layout.setContentsMargins(0, 0, 0, 0)

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        self.stack.addWidget(self.graph_page)

        # --- SIDE 1: TABEL ---
        self.table_page = QWidget()
        table_layout = QVBoxLayout(self.table_page)
        table_layout.setContentsMargins(0, 5, 0, 0)

        self.lbl_table_summary = QLabel("Styrkeudvikling i tabelform")
        self.lbl_table_summary.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50; margin-bottom: 4px;")
        table_layout.addWidget(self.lbl_table_summary)

        self.table_strength = QTableWidget()
        self.table_strength.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_strength.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_strength.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_strength.setAlternatingRowColors(True)
        table_layout.addWidget(self.table_strength)

        self.stack.addWidget(self.table_page)
        layout.addWidget(self.stack)

        # Start på graf-visningen
        self._switch_view(0)

    def _switch_view(self, index: int):
        self.stack.setCurrentIndex(index)
        active_style = (
            "background-color: #2E7D32; color: white; font-weight: bold; "
            "padding: 5px 14px; border-radius: 4px; border: 1px solid #4CAF50;"
        )
        inactive_style = (
            "background-color: #333333; color: #cccccc; font-weight: normal; "
            "padding: 5px 14px; border-radius: 4px; border: 1px solid #555555;"
        )
        if index == 0:
            self.btn_show_graph.setStyleSheet(active_style)
            self.btn_show_table.setStyleSheet(inactive_style)
        else:
            self.btn_show_graph.setStyleSheet(inactive_style)
            self.btn_show_table.setStyleSheet(active_style)

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

    def populate_strength_table(self, df: pd.DataFrame | None, selected_exercise: str = "Alle øvelser"):
        self.table_strength.clear()
        if df is None or df.empty:
            self.table_strength.setRowCount(0)
            self.table_strength.setColumnCount(0)
            self.lbl_table_summary.setText("Ingen data at vise.")
            return

        cols = list(df.columns)
        self.table_strength.setColumnCount(len(cols))
        self.table_strength.setHorizontalHeaderLabels(cols)
        self.table_strength.setRowCount(len(df))

        if selected_exercise == "Alle øvelser" or not selected_exercise:
            total_kg = df["Ændring (kg)"].sum() if "Ændring (kg)" in df.columns else 0.0
            sign = "+" if total_kg >= 0 else ""
            self.lbl_table_summary.setText(
                f"Oversigt over alle øvelser  |  Samlet fremgang på tværs af øvelser: {sign}{total_kg:g} kg"
            )
        else:
            last_diff = df["Ændring siden start (kg)"].iloc[-1] if "Ændring siden start (kg)" in df.columns else 0.0
            sign = "+" if last_diff >= 0 else ""
            self.lbl_table_summary.setText(
                f"Historik for {selected_exercise}  |  Samlet udvikling siden start: {sign}{last_diff:g} kg"
            )

        bold_font = QFont()
        bold_font.setBold(True)

        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, col_name in enumerate(cols):
                val = row[col_name]

                if "Ændring" in col_name and isinstance(val, (int, float)):
                    sign = "+" if val > 0 else ""
                    if "(%)" in col_name:
                        text = f"{sign}{val:.1f} %"
                    else:
                        text = f"{sign}{val:g} kg"
                    item = QTableWidgetItem(text)
                    item.setFont(bold_font)
                    if val > 0:
                        item.setForeground(QColor("#66BB6A"))  # Grøn ved stigning
                    elif val < 0:
                        item.setForeground(QColor("#EF5350"))  # Rød ved fald
                    else:
                        item.setForeground(QColor("#B0B0B0"))  # Grå ved 0
                else:
                    item = QTableWidgetItem(str(val))

                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if col_idx > 0 else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table_strength.setItem(row_idx, col_idx, item)

        header = self.table_strength.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for c in range(1, len(cols)):
            header.setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)

    def draw_data(self, plot_df: pd.DataFrame | None):
        self.figure.clear()

        if plot_df is not None and not plot_df.empty:
            ax = self.figure.add_subplot(111)
            val_col = "Værdi" if "Værdi" in plot_df.columns else "Estimeret_1RM"
            is_overall_kg = "Samlet fremgang (kg)" in plot_df["Øvelse"].values

            for ovelse, gruppe in plot_df.groupby("Øvelse"):
                gruppe = gruppe.sort_values("Dato")
                if is_overall_kg:
                    sidste_kg = gruppe[val_col].iloc[-1]
                    fortegn = "+" if sidste_kg >= 0 else ""
                    label_str = f"Samlet ændring på tværs af øvelser: {fortegn}{sidste_kg:g} kg"
                    
                    if "Top_Bidrag" in gruppe.columns and gruppe["Top_Bidrag"].iloc[-1]:
                        label_str += f"\nStørste stigninger: {gruppe['Top_Bidrag'].iloc[-1]}"

                    ax.plot(
                        gruppe["Dato"], 
                        gruppe[val_col], 
                        marker="o", 
                        linewidth=3, 
                        color="#2E7D32",
                        label=label_str
                    )

                    ax.fill_between(
                        gruppe["Dato"], gruppe[val_col], 0,
                        where=(gruppe[val_col] >= 0),
                        color="#4CAF50", alpha=0.18, interpolate=True
                    )
                    ax.fill_between(
                        gruppe["Dato"], gruppe[val_col], 0,
                        where=(gruppe[val_col] < 0),
                        color="#E53935", alpha=0.18, interpolate=True
                    )
                    ax.axhline(0, color="#666666", linestyle="--", linewidth=1.2, alpha=0.8)

                    for _, row in gruppe.iterrows():
                        v = row[val_col]
                        sign = "+" if v > 0 else ""
                        ax.annotate(
                            f"{sign}{v:g} kg",
                            (row["Dato"], v),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha="center",
                            fontsize=8.5,
                            fontweight="bold",
                            color="#1B5E20" if v >= 0 else "#B71C1C"
                        )
                else:
                    first_val = gruppe[val_col].iloc[0]
                    last_val = gruppe[val_col].iloc[-1]
                    diff_kg = last_val - first_val
                    fortegn = "+" if diff_kg >= 0 else ""
                    ax.plot(
                        gruppe["Dato"], 
                        gruppe[val_col], 
                        marker="o", 
                        linewidth=2.5, 
                        color="#1E88E5",
                        label=f"{ovelse} ({fortegn}{diff_kg:g} kg siden start)"
                    )

                    if "Reps" in gruppe.columns:
                        for _, row in gruppe.iterrows():
                            ax.annotate(
                                f"{row[val_col]:g}kg × {int(row['Reps'])}",
                                (row["Dato"], row[val_col]),
                                textcoords="offset points",
                                xytext=(0, 8),
                                ha="center",
                                fontsize=8,
                                fontweight="bold"
                            )

            if is_overall_kg:
                ax.set_title("Samlet Styrkeudvikling (Summen af ekstra kilo på tværs af alle øvelser)", fontsize=11, fontweight="bold")
                ax.set_ylabel("Samlet ændring i belastning (kg)")
            else:
                ax.set_title("Styrkeudvikling for valgt øvelse (kg i sæt)", fontsize=12, fontweight="bold")
                ax.set_ylabel("Vægt i sæt (kg)")

            ymin, ymax = ax.get_ylim()
            ax.set_ylim(ymin, ymax + (ymax - ymin) * 0.15 + 1)

            ax.set_xlabel("Dato")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(loc="upper left")

            self.figure.autofmt_xdate()
            self.figure.tight_layout()

        self.canvas.draw()