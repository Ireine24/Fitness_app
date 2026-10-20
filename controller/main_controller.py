class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Knyt knapper fra view til controller-metoder
        self.view.refresh_btn.bind(on_press=self.handle_refresh)
        self.view.save_btn.bind(on_press=self.handle_save)

    def handle_refresh(self, instance):
        self.model.load_data()
        self.view.update_data_view()

    def handle_save(self, instance):
        try:
            dato = self.view.input_dato.text
            ovelse = self.view.input_ovelse.text
            vaegt = float(self.view.input_vaegt.text)
            reps = int(self.view.input_reps.text)

            self.model.add_entry(dato, ovelse, vaegt, reps)
            self.view.lbl_status.text = "Sæt gemt succesfuldt!"
            self.view.update_data_view()
        except Exception as e:
            self.view.lbl_status.text = f"Fejl: {str(e)}"
