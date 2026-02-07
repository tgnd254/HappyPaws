
import uuid
from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.popup import Popup
from widgets import ImageButton,RoundedButton,RoundedBox,show_message
from utils import load_events,load_resources,save_events,resources_available

class RecurrenceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        root.add_widget(Label(
            text="Configurar recurrencia",
            color=(0.251, 0.765, 0.851, 1),
            font_name="fonts/poppins-bold.ttf",
            font_size="35sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        ))

        # Campo para la recurrencia
        box_recurrence = RoundedBox(size_hint=(0.5,0.1), pos_hint={"center_x":0.5,"center_y":0.7})
        self.input_recurrence = TextInput(
            hint_text="Recurrencia (diaria/semanal/mensual)",
            background_color=(0,0,0,0),
            font_name="fonts/OpenSans-Bold.ttf",
            foreground_color=(0.251, 0.765, 0.851, 1),
            font_size="20sp",
            multiline=False
        )
        box_recurrence.add_widget(self.input_recurrence)
        root.add_widget(box_recurrence)

        # Campo para la fecha de finalización
        box_until = RoundedBox(size_hint=(0.5,0.1), pos_hint={"center_x":0.5,"center_y":0.5})
        self.input_until = TextInput(
            hint_text="Repetir hasta (YYYY-MM-DD)",
            background_color=(0,0,0,0),
            font_name="fonts/OpenSans-Bold.ttf",
            foreground_color=(0.251, 0.765, 0.851, 1),
            font_size="20sp",
            multiline=False
        )
        box_until.add_widget(self.input_until)
        root.add_widget(box_until)

        # Botón para continuar
        btn_continue = ImageButton(
            source="images/check..png",
            size_hint=(None, None),
            pos_hint={"center_x": 0.90, "center_y": 0.09},
            size=(150,150),
            allow_stretch=True,
            keep_ratio=True,
        )
        btn_continue.bind(on_press=self.process_recurrence)
        root.add_widget(btn_continue)

        # Botón para volver
        def go_back(inst):
            self.manager.current="date"

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

    # Método para procesar la recurrencia
    def process_recurrence(self, *args):

        start = self.manager.temp_start
        end = self.manager.temp_end
        title = self.manager.temp_title
        resources = self.manager.temp_resources

        recurrence = self.input_recurrence.text.strip().lower() 
        until_text = self.input_until.text.strip()

        # Mostrar mensaje de error si el formato es inválido
        try:
            until = datetime.strptime(until_text, "%Y-%m-%d")
        except:
            show_message("Formato inválido para. Use YYYY-MM-DD")
            return

        # Mostrar mensaje de error si la fecha 'Repetir hasta' es inferior a la de fin
        if until.date() < end.date():
            show_message("La fecha 'Repetir hasta' debe ser posterior al fin del evento")
            return

        # Mostrar mensaje de error si la recurrencia excede un año
        if isinstance(start, str): 
            start = datetime.strptime(start, "%Y-%m-%d %H:%M")
        if (until - start).days > 365:
            show_message("Los datos del refugio son restaurados cada año. La recurrencia no puede exceder este tiempo")
            return

        # Determinar el intervalo de recurrencia
        if recurrence == "diaria":
            delta = timedelta(days=1)
        elif recurrence == "semanal":
            delta = timedelta(weeks=1)
        elif recurrence == "mensual":
            delta = timedelta(days=30)
        else:
            show_message("Recurrencia inválida. Use diaria/semanal/mensual")
            return

        occurrences = []
        current = start
        # Generar todas las ocurrencias
        while current <= until:
            occurrences.append((current, current + (end - start)))
            current += delta

        events = load_events()
        resources_info = load_resources()
        conflicts = []

        # Verificar conflictos de recursos para cada ocurrencia
        for occ_start, occ_end in occurrences:
            sug_start, sug_end, occupied = resources_available(occ_start, occ_end, resources, resources_info, events)
            if sug_start != occ_start or sug_end != occ_end:
                conflicts.append((occ_start, occ_end, sug_start, sug_end, occupied))

        # Si hay conflictos, mostrar sugerencias
        text=""
        if conflicts:
            for occ_start, occ_end, sug_start, sug_end, occupied in conflicts:
                text_resources='\n'.join(occupied)
                text+=f"En la fecha de {occ_start.strftime('%Y-%m-%d %H:%M')} a {occ_end.strftime('%Y-%m-%d %H:%M')}\n"+f"Estos recursos se encuentran ocupados:\n{text_resources}\n"+f"Te sugiero realizar tu evento: de {sug_start.strftime('%Y-%m-%d %H:%M')} a {sug_end.strftime('%Y-%m-%d %H:%M')}\n"
            show_message(text)
            return

        series_id = str(uuid.uuid4()) # Generar un ID único para la serie

        # Agregar eventos al json
        for occ_start, occ_end in occurrences:
            events.append({
                "title": title,
                "start": occ_start.strftime("%Y-%m-%d %H:%M"),
                "end": occ_end.strftime("%Y-%m-%d %H:%M"),
                "recurrence": recurrence,
                "until": until_text,
                "resources": resources,
                "place": self.manager.selected_place,
                "series_id": series_id
            })
        save_events(events)
        
        show_message("Evento recurrente creado exitosamente", color=(0, 0.6, 0, 1))
