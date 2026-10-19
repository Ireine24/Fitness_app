from __future__ import annotations
import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def draw_data(self, daglig_max: pd.DataFrame | None):
        self.figure.clear()

        if daglig_max is not None and not daglig_max.empty:
            ax = self.figure.add_subplot(111)
            for ovelse, gruppe in daglig_max.groupby("Øvelse"):
                gruppe = gruppe.sort_values("Dato")
                ax.plot(
                    gruppe["Dato"], 
                    gruppe["Estimeret_1RM"], 
                    marker="o", 
                    linewidth=2, 
                    label=ovelse
                )

            ax.set_title("Styrkeudvikling (Estimeret 1RM)", fontsize=12, fontweight="bold")
            ax.set_xlabel("Dato")
            ax.set_ylabel("Estimeret 1RM (kg)")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(loc="upper left")

            self.figure.autofmt_xdate()
            self.figure.tight_layout()

        self.canvas.draw()