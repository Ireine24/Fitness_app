from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

class ProgramScreen(Screen):
    def __init__(self, model, **kwargs):
        super(ProgramScreen, self).__init__(**kwargs)
        self.model = model
        
        # Hovedlayout med mørkegrå baggrund
        root_layout = BoxLayout(orientation='vertical')
        with root_layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.root_rect = Rectangle(size=self.size, pos=self.pos)
        root_layout.bind(size=self._update_root_rect, pos=self._update_root_rect)
        
        # Top-bar med Tilbage-knap og titel
        top_bar = BoxLayout(size_hint_y=0.1, padding=10)
        back_btn = Button(text="< Tilbage", size_hint_x=0.15, background_color=[0.25, 0.25, 0.25, 1])
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home_screen'))
        top_bar.add_widget(back_btn)
        
        title_lbl = Label(text="[b]Træningsprogram 2026 - Styrketræning[/b]", markup=True, font_size=22, halign='center', color=[1, 1, 1, 1])
        title_lbl.bind(size=lambda s, w: setattr(s, 'text_size', w))
        top_bar.add_widget(title_lbl)
        root_layout.add_widget(top_bar)

        # Rullebar til hele ugeskemaet
        scroll = ScrollView(size_hint=(1, 0.9))
        
        # Vandret boks der holder alle 7 ugedags-kolonner og strækker sig i bredden
        columns_container = BoxLayout(orientation='horizontal', size_hint=(1, None), spacing=4, padding=10)
        columns_container.bind(minimum_height=columns_container.setter('height'))

        days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        
        # Hent øvelser for alle dage og find max antal rækker
        day_exercises = {}
        max_rows = 1
        for day in days:
            exs = self.model.get_program_for_day(day)
            if not exs:
                exs = [("Hviledag", "")]
            day_exercises[day] = exs
            if len(exs) > max_rows:
                max_rows = len(exs)

        # Byg kolonne for kolonne (hver kolonne tager nu 1/7 af skærmens bredde)
        for day in days:
            col_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=4)
            col_box.bind(minimum_height=col_box.setter('height'))
            
            # 1. Ugedags-overskrift i toppen
            header_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50, padding=2)
            with header_box.canvas.before:
                Color(0.2, 0.2, 0.2, 1)
                header_box.bg_rect = Rectangle(size=header_box.size, pos=header_box.pos)
            header_box.bind(size=lambda inst, val, b=header_box: setattr(b.bg_rect, 'size', inst.size),
                            pos=lambda inst, val, b=header_box: setattr(b.bg_rect, 'pos', inst.pos))
            
            header_lbl = Label(
                text=f"[b]{day}[/b]", 
                markup=True, 
                font_size=16, 
                color=[0.2, 0.9, 0.4, 1], 
                halign='center',
                valign='middle'
            )
            header_lbl.bind(size=lambda s, w: setattr(s, 'text_size', w))
            header_box.add_widget(header_lbl)
            col_box.add_widget(header_box)

            # 2. Tilføj øvelserne ned ad kolonnen som tabel-celler
            exs = day_exercises[day]
            for i in range(max_rows):
                cell_box = BoxLayout(orientation='vertical', size_hint_y=None, height=85, padding=4)
                
                with cell_box.canvas.before:
                    Color(0.16, 0.16, 0.16, 1)
                    cell_box.bg_rect = Rectangle(size=cell_box.size, pos=cell_box.pos)
                cell_box.bind(size=lambda inst, val, b=cell_box: setattr(b.bg_rect, 'size', inst.size),
                                pos=lambda inst, val, b=cell_box: setattr(b.bg_rect, 'pos', inst.pos))

                if i < len(exs):
                    ex_name, sets_reps = exs[i]
                    
                    name_lbl = Label(
                        text=f"[b]{ex_name}[/b]", 
                        markup=True, 
                        font_size=13, 
                        color=[1, 1, 1, 1], 
                        halign='center',
                        valign='middle'
                    )
                    name_lbl.bind(size=lambda s, w: setattr(s, 'text_size', w))
                    cell_box.add_widget(name_lbl)
                    
                    if sets_reps:
                        reps_lbl = Label(
                            text=f"{sets_reps}", 
                            font_size=12, 
                            color=[1, 0.4, 0.4, 1], 
                            halign='center',
                            valign='middle'
                        )
                        reps_lbl.bind(size=lambda s, w: setattr(s, 'text_size', w))
                        cell_box.add_widget(reps_lbl)
                else:
                    empty_lbl = Label(text="", size_hint_y=None, height=85)
                    cell_box.add_widget(empty_lbl)
                
                col_box.add_widget(cell_box)

            columns_container.add_widget(col_box)

        scroll.add_widget(columns_container)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def _update_root_rect(self, instance, value):
        self.root_rect.size = instance.size
        self.root_rect.pos = instance.pos