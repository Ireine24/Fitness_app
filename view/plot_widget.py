from __future__ import annotations
import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Top-bar inde på graf-fanen med valg af øvelse
        filter_layout = QHBoxLayout()
        lbl_filter = QLabel("Vælg øvelse til graf:")
        lbl_filter.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50;")
        filter_layout.addWidget(lbl_filter)

        self.combo_ovelse = QComboBox()
        self.combo_ovelse.addItem("Alle øvelser")
        self.combo_ovelse.setMinimumWidth(220)
        filter_layout.addWidget(self.combo_ovelse)
        filter_layout.addStretch()

        layout.addLayout(filter_layout)

        # Graf og toolbar
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

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

    def draw_data(self, daglig_max: pd.DataFrame | None):
        self.figure.clear()

        if daglig_max is not None and not daglig_max.empty:
            ax = self.figure.add_subplot(111)
            is_average = "Gennemsnitlig samlet styrke" in daglig_max["Øvelse"].values

            for ovelse, gruppe in daglig_max.groupby("Øvelse"):
                gruppe = gruppe.sort_values("Dato")
                if is_average:
                    ax.plot(
                        gruppe["Dato"], 
                        gruppe["Estimeret_1RM"], 
                        marker="o", 
                        linewidth=3, 
                        color="#4CAF50",
                        label="Gennemsnitlig samlet 1RM"
                    )
                else:
                    ax.plot(
                        gruppe["Dato"], 
                        gruppe["Estimeret_1RM"], 
                        marker="o", 
                        linewidth=2, 
                        label=ovelse
                    )

            title_text = "Samlet gennemsnitlig styrkeudvikling" if is_average else "Styrkeudvikling (Estimeret 1RM)"
            ax.set_title(title_text, fontsize=12, fontweight="bold")
            ax.set_xlabel("Dato")
            ax.set_ylabel("Estimeret 1RM (kg)")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(loc="upper left")

            self.figure.autofmt_xdate()
            self.figure.tight_layout()

        self.canvas.draw()