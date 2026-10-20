from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from datetime import date

# Vi laver en brugerdefineret knap-boks, der garanterer, at teksten står centreret
class CardButton(ButtonBehavior, BoxLayout):
    def __init__(self, title, callback, **kwargs):
        super(CardButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 180
        self.padding = 15
        
        # Gør den trykbar
        self.bind(on_release=callback)
        
        # Tegn mørkegrå baggrund med runde hjørner
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[12])
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Centreret tekst-label
        self.lbl = Label(
            text=title,
            font_size=18,
            bold=True,
            color=[1, 1, 1, 1],
            halign='center',
            valign='middle'
        )
        # Tving label til at kende sin fulde størrelse, så den centrerer perfekt
        self.lbl.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        self.add_widget(self.lbl)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class HomeScreen(Screen):
    def __init__(self, model, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.model = model
        
        # Mørk baggrund til hele skærmen
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        root_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = BoxLayout(size_hint_y=0.1)
        header.add_widget(Label(text=date.today().strftime("%A, %d. %B %Y"), font_size=18, bold=True, halign='left', color=[1, 1, 1, 1]))
        header.add_widget(Label(text="Fitness Overblik", font_size=18, bold=True, halign='right', color=[0.6, 0.6, 0.6, 1]))
        root_layout.add_widget(header)

        # Gitter til kort (2x2)
        cards_layout = GridLayout(cols=2, spacing=20, size_hint_y=None, padding=[0, 10])
        cards_layout.bind(minimum_height=cards_layout.setter('height'))

        # Tilføj de 4 kort med præcis navigation
        cards_layout.add_widget(CardButton("Mit træningsprogram", lambda x: setattr(self.manager, 'current', 'program_screen')))
        cards_layout.add_widget(CardButton("Træningsøvelser udvikling", lambda x: setattr(self.manager, 'current', 'dev_screen')))
        cards_layout.add_widget(CardButton("Min vægt", lambda x: setattr(self.manager, 'current', 'weight_screen')))
        cards_layout.add_widget(CardButton("", lambda x: None)) # Tomt fjerde felt

        scroll = ScrollView(size_hint=(1, 0.9))
        scroll.add_widget(cards_layout)
        root_layout.add_widget(scroll)
        
        self.add_widget(root_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos