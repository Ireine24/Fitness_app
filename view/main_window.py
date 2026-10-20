from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import datetime

class MainWindow(TabbedPanel):
    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.do_default_tab = False

        # Opret faner
        self.setup_sets_tab()
        self.setup_add_tab()

    def setup_sets_tab(self):
        tab = TabbedPanelItem(text='Træningssæt')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.data_label = Label(text=self.get_sets_text(), halign='left', valign='top')
        self.data_label.bind(size=self.data_label.setter('text_size'))
        layout.add_widget(self.data_label)

        self.refresh_btn = Button(text='Opdater liste', size_hint_y=None, height=50)
        layout.add_widget(self.refresh_btn)

        tab.add_widget(layout)
        self.add_widget(tab)

    def setup_add_tab(self):
        tab = TabbedPanelItem(text='Tilføj Sæt')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text='Dato (YYYY-MM-DD):'))
        self.input_dato = TextInput(text=str(datetime.date.today()), multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.input_dato)

        layout.add_widget(Label(text='Øvelse:'))
        self.input_ovelse = TextInput(text='Bænkpres', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.input_ovelse)

        layout.add_widget(Label(text='Vægt (kg):'))
        self.input_vaegt = TextInput(text='80', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.input_vaegt)

        layout.add_widget(Label(text='Reps:'))
        self.input_reps = TextInput(text='8', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.input_reps)

        self.save_btn = Button(text='Gem sæt i database', size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.3, 1))
        layout.add_widget(self.save_btn)

        self.lbl_status = Label(text='', size_hint_y=None, height=30)
        layout.add_widget(self.lbl_status)

        tab.add_widget(layout)
        self.add_widget(tab)

    def get_sets_text(self):
        if self.model.df is not None and not self.model.df.empty:
            lines = []
            for _, row in self.model.df.head(15).iterrows():
                lines.append(f"{row['dato']} | {row['ovelse']} | {row['vaegt']} kg x {row['reps']} reps")
            return "\n".join(lines)
        return "Ingen data fundet i databasen endnu."

    def update_data_view(self):
        self.data_label.text = self.get_sets_text()
