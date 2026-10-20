from kivy.app import App
from model.fitness_model import FitnessModel
from controller.main_controller import MainController
from view.main_window import MainWindow

class FitnessApp(App):
    def build(self):
        self.title = "Fitness App"
        
        # Initialiser Model, View og Controller
        self.model = FitnessModel(db_path="fitness.db")
        self.model.load_data()
        
        self.view = MainWindow(model=self.model)
        self.controller = MainController(model=self.model, view=self.view)
        
        return self.view

if __name__ == "__main__":
    FitnessApp().run()
