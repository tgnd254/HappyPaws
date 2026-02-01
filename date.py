import json
from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior

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

def resources_available(start,end,resources,events):
    duration = end - start

    sorted_events = sorted(events, key=lambda ev: ev["start"])

    current_start = start
    current_end = end

    while True:
        conflicts = []
        occupated_resources_set=set()
        for ev in sorted_events:
            occupated_resources = [r for r in resources if r in ev["resources"]]
            if occupated_resources:
                ev_start = datetime.strptime(ev["start"], "%Y-%m-%d %H:%M")
                ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M")
                if not (current_start >= ev_end or current_end <= ev_start):
                    conflicts.append((ev_start, ev_end, occupated_resources))
                    occupated_resources_set.update(occupated_resources)
        if not conflicts:
            return current_start, current_end, list(occupated_resources_set)
        last_end = max(conflicts, key=lambda x: x[1])[1]
        current_start = last_end
        current_end = last_end + duration
        return current_start,current_end,list(occupated_resources_set)
    
class DateScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        self.events = load_events()
    def on_pre_enter(self):
        self.clear_widgets()
        root=FloatLayout()

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

        self.input_start=TextInput(
            hint_text="Inicio (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.3, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.75}
        )
        root.add_widget(self.input_start)

        self.input_end=TextInput(
            hint_text="Fin (YYYY-MM-DD HH:MM)",
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1),
            multiline=False,
            size_hint=(0.3, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        root.add_widget(self.input_end)

        self.msg_box = BoxLayout(
            orientation="vertical", 
            size_hint=(0.8, 0.3), 
            pos_hint={"center_x": 0.5, "center_y": 0.30})
        root.add_widget(self.msg_box)

        btn_confirm = Button(
            text="Confirmar",
            color=(1,1,1,1),
            bold=True,
            font_name="fonts/SHOWG.TTF",
            size_hint=(0.15, 0.1),
            pos_hint={"center_x": 0.85, "center_y": 0.07},
            background_color=(0.251, 0.878, 0.816, 1)
        )
        btn_confirm.bind(on_press=self.create_event)
        root.add_widget(btn_confirm)

        def go_back(inst):
            self.manager.current="resources"
        btn_back = ImageButton(
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

    def create_event(self,instance):
        self.msg_box.clear_widgets()
        start_str = self.input_start.text.strip()
        end_str = self.input_end.text.strip()
        try:
            start=datetime.strptime(start_str,"%Y-%m-%d %H:%M")
            end=datetime.strptime(end_str,"%Y-%m-%d %H:%M")
        except ValueError:
            msg = Label(
                text="Formato inválido", 
                font_size="18sp",
                color=(0.447, 0.184, 0.216, 1),
                bold=True,
                font_name="fonts/GILSANUB.TTF"
            )
            self.msg_box.add_widget(msg) 
            return
        if end<=start:
            msg = Label(
                text="La fecha de fin debe ser posterior a la de inicio", 
                font_size="18sp",
                color=(0.447, 0.184, 0.216, 1),
                bold=True,
                font_name="fonts/GILSANUB.TTF"
            )
            self.msg_box.add_widget(msg)
            return
        
        resources = self.manager.selected_resources
        newstart,newend,occupated_resources=resources_available(start,end,resources,self.events)

        if(newstart,newend)!=(start,end):
            msg_resources = Label(
                text="Recursos Ocupados: ".join(occupated_resources),
                font_size="16sp",
                color=(0.447, 0.184, 0.216, 1),
                bold=True,
                font_name="fonts/GILSANUB.TTF"
            )
            self.msg_box.add_widget(msg_resources)

            msg_date = Label(
                text=f"Fecha Sugerida: {newstart} a {newend}", 
                font_size="16sp",
                color=(0.447, 0.184, 0.216, 1),
                bold=True,
                font_name="fonts/GILSANUB.TTF"
            )
            self.msg_box.add_widget(msg_date)

        else:
            new_event = {
                "start": start.strftime("%Y-%m-%d %H:%M"),
                "end": end.strftime("%Y-%m-%d %H:%M"),
                "resources": resources,
                "place": self.manager.selected_place
            }
            self.events.append(new_event)
            save_events(self.events)
            msg_event = Label(
                text=f"Evento creado exitosamente", 
                font_size="16sp",
                color=(0.388, 0.420, 0.184, 1),
                bold=True,
                font_name="fonts/GILSANUB.TTF"
            )
            self.msg_box.add_widget(msg_event)







    




                




    

