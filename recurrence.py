
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

from date import load_events, save_events, load_resources, resources_available

class ImageButton(ButtonBehavior, Image): 
    pass

class RecurrenceScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        root.add_widget(Label(
            text="Configurar recurrencia",
            font_name="fonts/SHOWG.TTF",
            font_size="25sp",
            color=(0, 0.5, 0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        ))

        self.input_recurrence = TextInput(
            hint_text="Recurrencia (diaria/semanal/mensual)",
            size_hint=(0.5, 0.06),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1)
        )
        root.add_widget(self.input_recurrence)

        self.input_until = TextInput(
            hint_text="Repetir hasta (YYYY-MM-DD)",
            size_hint=(0.5, 0.06),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            background_color=(0.6, 1, 0.6, 1),
            foreground_color=(0.2078, 0.4980, 0.7294, 1)
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
        btn_continue.bind(on_press=self.process_recurrence)
        root.add_widget(btn_continue)

        def go_back(inst):
            self.manager.current="date"

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

    def process_recurrence(self, *args):
        self.error_box.clear_widgets()
        start = self.manager.temp_start
        end = self.manager.temp_end
        title = self.manager.temp_title
        resources = self.manager.temp_resources

        recurrence = self.input_recurrence.text.strip().lower()
        until_text = self.input_until.text.strip()

        try:
            until = datetime.strptime(until_text, "%Y-%m-%d")
        except:
            self.show_message("Formato inválido para. Use YYYY-MM-DD")
            return

        if until.date() < end.date():
            self.show_message("La fecha 'Repetir hasta' debe ser posterior al fin del evento")
            return

        if (until - start).days > 365:
            self.show_message("Los datos del refugio son restaurados cada año. La recurrencia no puede exceder este tiempo")
            return

        if recurrence == "diaria":
            delta = timedelta(days=1)
        elif recurrence == "semanal":
            delta = timedelta(weeks=1)
        elif recurrence == "mensual":
            delta = timedelta(days=30)
        else:
            self.show_message("Recurrencia inválida. Use diaria/semanal/mensual")
            return

        occurrences = []
        current = start
        while current <= until:
            occurrences.append((current, current + (end - start)))
            current += delta

        events = load_events()
        resources_info = load_resources()
        conflicts = []

        for occ_start, occ_end in occurrences:
            sug_start, sug_end, occupied = resources_available(occ_start, occ_end, resources, resources_info, events)
            if sug_start != occ_start or sug_end != occ_end:
                conflicts.append((occ_start, occ_end, sug_start, sug_end, occupied))

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
        self.show_message("Evento recurrente creado exitosamente", color=(0, 0.6, 0, 1))
