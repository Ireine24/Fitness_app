from kivy.uix.screenmanager import ScreenManager
from view.home_screen import HomeScreen
from view.program_screen import ProgramScreen
from view.placeholder_screen import PlaceholderScreen

class MainWindow(ScreenManager):
    def __init__(self, model, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.model = model
        
        # Samler skærmene
        self.add_widget(HomeScreen(model=self.model, name='home_screen'))
        self.add_widget(ProgramScreen(model=self.model, name='program_screen'))
        self.add_widget(PlaceholderScreen("Træningsøvelser udvikling", name='dev_screen'))
        self.add_widget(PlaceholderScreen("Min vægt", name='weight_screen'))