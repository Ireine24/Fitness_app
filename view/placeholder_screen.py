from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class PlaceholderScreen(Screen):
    def __init__(self, title, **kwargs):
        super(PlaceholderScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)
        
        top_bar = BoxLayout(size_hint_y=0.1)
        back_btn = Button(text="< Tilbage", size_hint_x=0.2)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home_screen'))
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Label(text=f"[b]{title}[/b]", markup=True, font_size=20))
        layout.add_widget(top_bar)
        
        layout.add_widget(Label(text=f"Her vises {title.lower()} snart...", font_size=18))
        self.add_widget(layout)