from model.fitness_model import FitnessModel
from view.plot_widget import PlotWidget


class PlotController:
    def __init__(self, model: FitnessModel, plot_widget: PlotWidget):
        self.model = model
        self.plot_widget = plot_widget

    def update_plot(self, selected_exercise: str):
        data = self.model.get_aggregated_plot_data(selected_exercise)
        self.plot_widget.draw_data(data)