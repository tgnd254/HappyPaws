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
from kivy.clock import Clock
from kivy.uix.popup import Popup
from widgets import ImageButton,RoundedButton,RoundedBox, show_message
from utils import load_events,load_resources,save_events,resources_available

load_events()

load_resources()

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
            color=(0.251, 0.765, 0.851, 1),
            font_name="fonts/poppins-bold.ttf",
            font_size="27sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        )
        root.add_widget(label)

        # Campo para el título del evento
        box_title = RoundedBox(size_hint=(0.5,0.1), pos_hint={"center_x":0.5,"center_y":0.8})
        self.input_title = TextInput(
            hint_text="Título del evento",
            background_color=(0,0,0,0),
            font_name="fonts/OpenSans-Bold.ttf",
            foreground_color=(0.251, 0.765, 0.851, 1),
            font_size="25sp",
            multiline=False
        )
        box_title.add_widget(self.input_title)
        root.add_widget(box_title)

        box_start = RoundedBox(size_hint=(0.5,0.1), pos_hint={"center_x":0.5,"center_y":0.6})
        self.input_start = TextInput(
            hint_text="Inicio (YYYY-MM-DD HH:MM)",
            background_color=(0,0,0,0),
            font_name="fonts/OpenSans-Bold.ttf",
            foreground_color=(0.251, 0.765, 0.851, 1),
            font_size="25sp",
            multiline=False
        )
        box_start.add_widget(self.input_start)
        root.add_widget(box_start)

        box_end = RoundedBox(size_hint=(0.5,0.1), pos_hint={"center_x":0.5,"center_y":0.4})
        self.input_end = TextInput(
            hint_text="Fin (YYYY-MM-DD HH:MM)",
            background_color=(0,0,0,0),
            font_name="fonts/OpenSans-Bold.ttf",
            foreground_color=(0.251, 0.765, 0.851, 1),
            font_size="25sp",
            multiline=False
        )
        box_end.add_widget(self.input_end)
        root.add_widget(box_end)

        # Botón para continuar
        btn_continue = ImageButton(
            source="images/check..png",
            size_hint=(None, None),
            pos_hint={"center_x": 0.90, "center_y": 0.09},
            size=(150,150),
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
            size=(130, 130),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.09,"center_y": 0.09}
        )
        btn_back.bind(on_press=go_back)
        root.add_widget(btn_back)

        self.add_widget(root)

    # Método para crear un evento
    def create_event(self, *args):
        
        #Se muestra error si no hay titulo
        title = self.input_title.text.strip() 
        if not title: 
            show_message("Debe introducir un título para el evento") 
            return

        # Se muestra errorno si el formato de la fecha de inicio o de la fecha de fin es incorrecto
        try:
            start = datetime.strptime(self.input_start.text.strip(), "%Y-%m-%d %H:%M")
            end = datetime.strptime(self.input_end.text.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            show_message("Formato inválido. Use YYYY-MM-DD HH:MM.")
            return

        # Se muestra error si la fecha de fin es anterior o igual a la de inicio
        if end <= start:
            show_message("La fecha de fin debe ser posterior a la de inicio")
            return
        
        # Validar que la fecha de inicio no sea anterior al momento actual
        now = datetime.now()
        if start < now:
            show_message("La fecha de inicio no puede ser anterior al momento actual")
            return


        resources = self.manager.selected_resources
        suggested_start, suggested_end, occupied = resources_available(start, end, resources, self.resources_info, self.events)

        # Si la fecha sugerida es distinta a la introducida por el horario entonces los recursos no estan disponibles
        if suggested_start != start:
            text_resources = "\n".join(occupied)
            show_message(
                f"Lo siento en esa fecha hay recursos ocupados:\n{text_resources}\n"
                f"Te sugiero realizar tu evento de {suggested_start} a {suggested_end}")
            return
        
        self.ask_recurrence(title, start, end, resources) 

    # Método para preguntar por la recurrencia del evento
    def ask_recurrence(self, title, start, end, resources):
        content = FloatLayout()
        with content.canvas.before: 
            Color(1.0, 0.627, 0.478, 1)
            border=RoundedRectangle(pos=content.pos, size=content.size, radius=[20]) 
            Color(1.0, 0.992, 0.906, 1) 
            bg=RoundedRectangle(pos=(content.x+3, content.y+3), size=(content.width-6, content.height-6), radius=[18]) 
        def update_rects(*args): 
            border.pos = content.pos 
            border.size = content.size 
            bg.pos = (content.x+3, content.y+3) 
            bg.size = (content.width-6, content.height-6) 
        content.bind(pos=update_rects, size=update_rects) 
        Clock.schedule_once(lambda dt: update_rects(), 0)

        lbl = Label( 
            text="¿Desea que este evento sea recurrente?", 
            font_size="22sp",
            font_name="fonts/OpenSans-Bold.ttf",
            color=(0.243, 0.153, 0.137, 1), 
            halign="center", 
            valign="middle", 
            size_hint=(1, None), 
            height=80, 
            pos_hint={"center_x": 0.5, "center_y": 0.75}, 
            text_size=(500, None)     
        ) 
        content.add_widget(lbl) 

        btns = BoxLayout(
            spacing=25, 
            size_hint=(None,None), 
            size=(540, 50), 
            pos_hint={"center_x": 0.65, "center_y": 0.35} 
        ) 

        btn_yes = RoundedButton(
            text="Sí", 
            background_color=(0.596, 0.984, 0.596, 1), 
            color=(1, 1, 1, 1),
            font_name="fonts/Roboto-Medium.ttf",
            size_hint=(None, None), 
            size=(160, 45), 
            font_size=25
        ) 
        btns.add_widget(btn_yes) 

        btn_no = RoundedButton(
            text="No", 
            background_color=(1.0, 0.627, 0.478, 1), 
            color=(1, 1, 1, 1),
            font_name="fonts/Roboto-Medium.ttf",
            size_hint=(None, None), 
            size=(160, 45), 
            font_size=25
        ) 
        btns.add_widget(btn_no) 
        
        content.add_widget(btns) 
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(None,None),
            auto_dismiss=False,
            size=(600,230),
            background="",
            background_color=(0,0,0,0), 
            separator_color=(0,0,0,0)
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
        show_message("Evento creado exitosamente", color=(0,0.5,0.5,1))

    # Método para ir a la pantalla de recurrencia
    def go_to_recurrence_screen(self, title, start, end, resources, popup):
        popup.dismiss()
        self.manager.temp_title = title
        self.manager.temp_start = start
        self.manager.temp_end = end
        self.manager.temp_resources = resources
        self.manager.current = "recurrence"