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


class ImageButton(ButtonBehavior, Image): 
    pass

def load_events():
    try:
        with open("events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_events(events):
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

def load_resources():
    with open("resources.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def resources_available(start,end,selected,resources,events):
    duration=end-start
    current_start,current_end=start,end
    occupated_resources_set=set()
    events_sorted = sorted(events, key=lambda ev: ev["start"])
    while True:
        unavailable=[]
        for sr in selected:
            count=0
            for r in resources:
                if r["name"]==sr:
                    quantity=r["quantity"]
                    break
            for ev in events_sorted:
                ev_start = datetime.strptime(ev["start"], "%Y-%m-%d %H:%M") 
                ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M") 
                if not (current_end <= ev_start or current_start >= ev_end):
                    if sr in ev["resources"]:
                        count+=1
            if count>=quantity:
                unavailable.append(sr)
        occupated_resources_set.update(unavailable)
        if not unavailable: 
            return current_start, current_end, list(occupated_resources_set)
        conflicts_ends=[]
        for ev in events_sorted:
            for r in unavailable:
                if r in ev["resources"]:
                    ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M") 
                    conflicts_ends.append(ev_end)
                    break
        if conflicts_ends:
            last_end=max(conflicts_ends)
        current_start=last_end
        current_end=current_start+duration
class DateScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        self.events = load_events()
        self.resources_info = load_resources()

    def update_bg(self,*args): 
        self.msg_bg.pos = self.msg_box.pos 
        self.msg_bg.size = self.msg_box.size

    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        label = Label(
            text="Introduce el horario en que desea realizar su evento",
            color=(0, 0.5, 0.5, 1),
            font_name="fonts/SHOWG.TTF",
            font_size="25sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        )
        root.add_widget(label)

        self.input_start = TextInput(
            hint_text="Inicio (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.8}
        )
        root.add_widget(self.input_start)

        self.input_end = TextInput(
            hint_text="Fin (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        root.add_widget(self.input_end)

        self.input_recurrence = TextInput( 
            hint_text="Recurrencia (ninguna/diaria/semanal/mensual)", 
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        root.add_widget(self.input_recurrence)

        self.input_until = TextInput( 
            hint_text="Repetir hasta (YYYY-MM-DD) (si es recurrente)", 
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        root.add_widget(self.input_until)

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

    def create_event(self, *args):
        self.error_box.clear_widgets()
        try: 
            start = datetime.strptime(self.input_start.text.strip(), "%Y-%m-%d %H:%M") 
            end = datetime.strptime(self.input_end.text.strip(), "%Y-%m-%d %H:%M") 
            until_text = self.input_until.text.strip()
            until = None
            if until_text:
                until = datetime.strptime(until_text, "%Y-%m-%d")  # solo fecha
        except ValueError: 
            self.show_message("Formato inválido. Use YYYY-MM-DD HH:MM para inicio/fin y YYYY-MM-DD para 'Repetir hasta'")
            return

        if end <= start:
            self.show_message("La fecha de fin debe ser posterior a la de inicio")
            return
        if until and until.date() < end.date(): 
            self.show_message("La fecha 'Repetir hasta' debe ser posterior a la fecha de fin del evento") 
            return

        recurrence = self.input_recurrence.text.strip().lower()
        if recurrence != "ninguna" and until:
            if (until - start).days > 365: 
                self.show_message("La información del refugio se actualiza cada año. Por favor limite la recurrencia a menos de un año.")
                return 

        occurrences = [] 
        if recurrence == "ninguna": 
            occurrences = [(start, end)] 
        else: 
            if recurrence == "diaria": 
                delta = timedelta(days=1) 
            elif recurrence == "semanal":
                delta = timedelta(weeks=1) 
            elif recurrence == "mensual": 
                delta = timedelta(days=30) 
            else: 
                self.show_message("Recurrencia inválida. Use ninguna/diaria/semanal/mensual") 
                return 

            current = start 
            while until and current <= until:
                occurrences.append((current, current + (end - start))) 
                current += delta

        resources = self.manager.selected_resources
        conflicts = []

        for occ_start, occ_end in occurrences:
            suggested_start, suggested_end, occupied = resources_available(
                occ_start, occ_end,
                selected=resources,
                resources=self.resources_info,
                events=self.events
            )
            if suggested_start != occ_start or suggested_end != occ_end:
                conflicts.append((occ_start, occ_end, suggested_start, suggested_end, occupied))

        if conflicts:
            for occ_start, occ_end, sug_start, sug_end, occupied in conflicts:
                text_resources='\n'.join(occupied)
                self.show_message(
                    f"En la fecha de {occ_start.strftime('%Y-%m-%d %H:%M')} a {occ_end.strftime('%Y-%m-%d %H:%M')} "
                    f"Estos recursos se encuentran ocupados:\n{text_resources}\n"
                )
            self.show_message(f"Te sugiero realizar tu evento: de {sug_start.strftime('%Y-%m-%d %H:%M')} a {sug_end.strftime('%Y-%m-%d %H:%M')}")
            return
        
        series_id = str(uuid.uuid4())  
        for occ_start, occ_end in occurrences:
            self.events.append({
                "start": occ_start.strftime("%Y-%m-%d %H:%M"),
                "end": occ_end.strftime("%Y-%m-%d %H:%M"),
                "recurrence": recurrence,
                "until": until.strftime("%Y-%m-%d") if until else None,
                "resources": resources,
                "place": self.manager.selected_place,
                "series_id": series_id   
            })
        save_events(self.events)
        self.show_message("Evento creado exitosamente", color=(0,0.6,0,1))

    

                    


