import json
import uuid
from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class ImageButton(ButtonBehavior, Image): 
    pass

# Método para cargar eventos
def load_events():
    try:
        with open("data/events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
# Método para guardar eventos
def save_events(events):
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

# Método para cargar recursos
def load_resources():
    with open("data/resources.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Método para verificar recursos disponibles
def resources_available(start,end,selected,resources,events):
    duration=end-start
    current_start,current_end=start,end
    occupated_resources_set=set() # Mantener registro de recursos ocupados
    events_sorted = sorted(events, key=lambda ev: ev["start"]) # Ordenar eventos por fecha de inicio

    while True:
        unavailable=[]
        for sr in selected:
            count=0 # Contador de eventos que utilizan el recurso

            # Obtener la cantidad del recurso
            for r in resources:
                if r["name"]==sr:
                    quantity=r["quantity"]
                    break

            for ev in events_sorted:
                ev_start = datetime.strptime(ev["start"], "%Y-%m-%d %H:%M") 
                ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M") 
                if not (current_end <= ev_start or current_start >= ev_end): # Verificar solapamiento
                    if sr in ev["resources"]:
                        count+=1

            # Verificar si el recurso está disponible
            if count>=quantity:
                unavailable.append(sr)

        occupated_resources_set.update(unavailable)

        # Si no hay recursos no disponibles devolver la fecha actual
        if not unavailable: 
            return current_start, current_end, list(occupated_resources_set)
        
        conflicts_ends=[]
        for ev in events_sorted:
            for r in unavailable:
                if r in ev["resources"]:
                    ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M") 
                    conflicts_ends.append(ev_end)
                    break

        # Si hay conflictos, avanzar al final del conflicto más cercano
        if conflicts_ends:
            last_end=max(conflicts_ends)

        current_start=last_end
        current_end=current_start+duration


class DateScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 

        self.events = load_events()
        self.resources_info = load_resources()

    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        label = Label(
            text="Introduzca el horario en que desea realizar su evento",
            color=(0, 0.5, 0.5, 1),
            font_name="fonts/SHOWG.TTF",
            font_size="25sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        )
        root.add_widget(label)

        # Campo para el título del evento
        self.input_title = TextInput(
            hint_text="Título del evento",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False, size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.8}
        )
        root.add_widget(self.input_title)

        # Campo para la fecha de inicio
        self.input_start = TextInput(
            hint_text="Inicio (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        root.add_widget(self.input_start)

        # Campo para la fecha de fin
        self.input_end = TextInput(
            hint_text="Fin (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        root.add_widget(self.input_end)

        # Scroll para mensajes de error
        self.error_scroll = ScrollView(
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            bar_color=(0.9, 0.1, 0.1, 1), 
            scroll_type=['bars']
        )

        with self.error_scroll.canvas.before: 
            Color(1, 0.9, 0.9, 0.8)
            self.error_bg = RoundedRectangle(radius=[10])

            def update_error_bg(*args):
                self.error_bg.pos = self.error_scroll.pos
                self.error_bg.size = self.error_scroll.size

            self.error_scroll.bind(pos=update_error_bg, size=update_error_bg)

        self.error_box = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=[10, 30, 10, 10]
        )
        self.error_box.bind(minimum_height=self.error_box.setter("height"))

        self.error_scroll.add_widget(self.error_box)

        root.add_widget(self.error_scroll)

        # Botón para continuar
        btn_continue = ImageButton(
            source="images/check..png",
            size_hint=(None, None),
            pos_hint={"center_x": 0.90, "center_y": 0.1},
            size=(60,60),
            allow_stretch=True,
            keep_ratio=True,
        )
        btn_continue.bind(on_press=self.create_event)
        root.add_widget(btn_continue)

        # Botón para volver
        def go_back(inst):
            self.manager.current="resources"

        btn_back = ImageButton (
            source="images/back.png",
            size_hint=(None, None),
            size=(60, 60),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.05,"center_y": 0.1}
        )
        btn_back.bind(on_press=go_back)
        root.add_widget(btn_back)

        self.add_widget(root)

    # Método para mostrar mensajes de error
    def show_message(self, text,color=(0.9,0.1,0.1,1)):
        lbl = Label(
            text=text,
            color=color,
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=45
        )
        self.error_box.add_widget(lbl)

    # Método para crear un evento
    def create_event(self, *args):
        self.error_box.clear_widgets()
        
        #Se muestra error si no hay titulo
        title = self.input_title.text.strip() 
        if not title: 
            self.show_message("Debe introducir un título para el evento") 
            return

        # Se muestra errorno si el formato de la fecha de inicio o de la fecha de fin es incorrecto
        try:
            start = datetime.strptime(self.input_start.text.strip(), "%Y-%m-%d %H:%M")
            end = datetime.strptime(self.input_end.text.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_message("Formato inválido. Use YYYY-MM-DD HH:MM.")
            return

        # Se muestra error si la fecha de fin es anterior o igual a la de inicio
        if end <= start:
            self.show_message("La fecha de fin debe ser posterior a la de inicio")
            return

        resources = self.manager.selected_resources
        suggested_start, suggested_end, occupied = resources_available(start, end, resources, self.resources_info, self.events)

        # Si la fecha sugerida es distinta a la introducida por el horario entonces los recursos no estan disponibles
        if suggested_start != start:
            text_resources = "\n".join(occupied)
            self.show_message(f"Lo siento en esa fecha hay recursos ocupados:\n{text_resources}\n")
            self.show_message(f"Te sugiero realizar tu evento de {suggested_start} a {suggested_end}")
            return
        
        self.ask_recurrence(title, start, end, resources) 

    # Método para preguntar por la recurrencia del evento
    def ask_recurrence(self, title, start, end, resources):
        content = BoxLayout(
            orientation="vertical", 
            spacing=20, 
            padding=20
        ) 

        lbl = Label( 
            text="¿Desea que este evento sea recurrente?", 
            font_name="fonts/ELEPHNT.TTF", 
            font_size="22sp", 
            color=(0, 0.5, 0.5, 1)
        ) 
        content.add_widget(lbl) 

        btns = BoxLayout(
            spacing=20, 
            size_hint_y=None, 
            height=40
        ) 

        btn_yes = Button(
            text="Sí", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1),
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        ) 
        btns.add_widget(btn_yes) 

        btn_no = Button(
            text="No", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1),
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        ) 
        btns.add_widget(btn_no) 
        
        content.add_widget(btns) 
        
        popup = Popup( 
            title="", 
            content=content, 
            size_hint=(0.6, 0.3), 
            auto_dismiss=False,
            background="", 
            separator_color=(1, 0.992, 0.815, 1),
            background_color=(1, 0.992, 0.815, 1) 
        ) 
        btn_no.bind(on_press=lambda inst: self.create_single_event(title, start, end, resources, popup)) 
        btn_yes.bind(on_press=lambda inst: self.go_to_recurrence_screen(title, start, end, resources, popup)) 
        popup.open()

    # Método para crear un evento unico
    def create_single_event(self, title, start, end, resources, popup):
        popup.dismiss()

        self.events.append({
            "title": title,
            "start": start.strftime("%Y-%m-%d %H:%M"),
            "end": end.strftime("%Y-%m-%d %H:%M"),
            "recurrence": "ninguna",
            "resources": resources,
            "place": self.manager.selected_place,
            "series_id": None
        }) 

        save_events(self.events) 
        self.show_message("Evento creado exitosamente", color=(0,0.5,0.5,1))

    # Método para ir a la pantalla de recurrencia
    def go_to_recurrence_screen(self, title, start, end, resources, popup):
        popup.dismiss()
        self.manager.temp_title = title
        self.manager.temp_start = start
        self.manager.temp_end = end
        self.manager.temp_resources = resources
        self.manager.current = "recurrence"