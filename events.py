import json
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle

class ImageButton(ButtonBehavior, Image): 
    pass

def load_events():
    try:
        with open("data/events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_events(events):
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

class EventsScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        self.events = load_events()

    def on_pre_enter(self):
        self.events = load_events()
        self.clear_widgets()
        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        label=Label(
            text="Eventos Creados",
            color=(0, 0.5, 0.5, 1),
            font_name="fonts/SHOWG.TTF",
            font_size="30sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95})
        root.add_widget(label)

        # ScrollView para la lista de eventos
        scroll = ScrollView(
            size_hint=(0.95, 0.8), 
            pos_hint={"center_x":0.5, "center_y":0.5},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            bar_color=(0,0.5,0.5,1), 
            scroll_type=['bars']
        ) 

        layout = GridLayout(cols=8, spacing=20, padding=40, size_hint_y=None, row_default_height=350, row_force_default=True) 
        layout.bind(minimum_height=layout.setter("height"))

        # Añadir eventos a la lista
        for idx, ev in enumerate(self.events):
            box = BoxLayout(orientation="vertical", size_hint=(None,None), width=200, height=300, spacing=5, padding=5)
            place=ev["place"]

            # Etiqueta del título del evento
            lbl = Label(
                text=ev["title"],
                font_size="22sp",
                bold=True,
                color=(0, 0.3, 0, 1),
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=60,
                text_size=(180, None)
            )
            box.add_widget(lbl)

            # Imagen del lugar
            img = Image(source=f"images/{place}.png",allow_stretch=True,mipmap=True, keep_ratio=False,size=(150,150))
            box.add_widget(img)

            # Botón para ver detalles del evento
            btn_details = Button(text="Ver detalles", size_hint_y=None, height=40,background_color=(0.6, 1, 0.6, 1),color=(1, 0.992, 0.815, 1))
            btn_details.bind(on_press=lambda inst, i=idx: self.show_details(i))
            box.add_widget(btn_details)

            # Botón para eliminar el evento
            btn_delete = Button(text="Eliminar", size_hint_y=None, height=40,background_color=(0.6, 1, 0.6, 1),color=(1, 0.992, 0.815, 1))
            btn_delete.bind(on_press=lambda inst, i=idx: self.confirm_delete(i))
            box.add_widget(btn_delete)

            layout.add_widget(box)

        scroll.add_widget(layout)

        root.add_widget(scroll)

        # Botón para volver a la pantalla principal
        def go_back(inst):
            self.manager.current="home"

        btn_back = ImageButton (
            source="images/back.png",
            size_hint=(None, None),
            size=(60, 60),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.05,"center_y": 0.05}
        )
        btn_back.bind(on_press=go_back)
        root.add_widget(btn_back)

        self.add_widget(root)

    # Función para confirmar la eliminación de un evento
    def confirm_delete(self, index):
        event = self.events[index]
        series_id = event.get("series_id", None)

        content = BoxLayout(orientation="vertical", spacing=20, padding=20)

        lbl = Label(
            text="¿Desea eliminar todas las ocurrencias de este evento?",
            font_name="fonts/ELEPHNT",
            font_size="23sp",
            bold=True,
            color=(0, 0.5, 0.5, 1)
        )
        content.add_widget(lbl)

        btns = BoxLayout(spacing=20, size_hint_y=None, height=40,width=30)

        btn_all = Button(
            text="Sí, todas", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1), 
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        )
        btns.add_widget(btn_all)

        btn_one = Button(
            text="No, solo esta", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1), 
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        )
        btns.add_widget(btn_one)

        btn_cancel = Button(
            text="Cancelar", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1), 
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        )
        btns.add_widget(btn_cancel)
        
        content.add_widget(btns)

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False,
            background="",
            background_color=(1, 0.992, 0.815, 1),
            separator_color=(1, 0.992, 0.815, 1)
        )

        btn_all.bind(on_press=lambda inst: self.delete_series(series_id, popup))
        btn_one.bind(on_press=lambda inst: self.delete_event(index, popup))
        btn_cancel.bind(on_press=popup.dismiss)

        popup.open()

    # Función para eliminar un evento solamente
    def delete_event(self, index, popup):
        del self.events[index]
        save_events(self.events)
        popup.dismiss()
        self.on_pre_enter()

    # Función para eliminar una serie de eventos
    def delete_series(self, series_id, popup):
        self.events = [ev for ev in self.events if ev.get("series_id") != series_id]
        save_events(self.events)
        popup.dismiss()
        self.on_pre_enter()

    # Función para mostrar los detalles de un evento
    def show_details(self,index):
        event = self.events[index]

        scroll = ScrollView(
            size_hint=(1,1), 
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            bar_color=(0,0.5,0.5,1), 
            scroll_type=['bars']
        ) 

        content = BoxLayout( 
            orientation="vertical", 
            spacing=18, 
            padding=[17, 15], 
            size_hint_y=None, 
            size_hint_x=1,
        ) 
        content.bind(minimum_height=content.setter("height"))

        start = event.get("start", "—") 
        end = event.get("end", "—") 
        resources = event.get("resources", []) 
        recurrence = event.get("recurrence", "No recurrente")

        # Etiqueta con la fecha de inicio y fin del evento
        content.add_widget(Label(
            text=f"Inicio: {start}\nFin: {end}",
            bold=True,
            font_name="fonts/ELEPHNT.TTF",
            font_size="20sp",
            color=(0, 0.5, 0.5, 1),
            size_hint_y=None,
            valign="middle", 
            size_hint_x=1, 
            text_size=(390, None),
            height=60 
        )) 

        # Etiqueta con los recursos del evento
        recursos_text = "Recursos:\n" + "\n".join(f"- {r}" for r in resources)
        content.add_widget(Label(
            text=recursos_text,
            bold=True,
            font_name="fonts/ELEPHNT.TTF",
            font_size="20sp",
            color=(0, 0.5, 0.5, 1),
            halign="left",
            valign="top",
            size_hint_y=None,
            size_hint_x=1,
            text_size=(390, None)  
        ))

        # Etiqueta con la recurrencia del evento
        content.add_widget(Label(
            text=f"Recurrencia: {recurrence}",
            bold=True,
            font_name="fonts/ELEPHNT.TTF",
            font_size="20sp",
            color=(0, 0.5, 0.5, 1),
            size_hint_y=None,
            valign="middle",
            size_hint_x=1,
            text_size=(390, None),
            height=40 
        )) 

        content.add_widget(Label(text=""))

        scroll.add_widget(content) 

        popup = Popup( 
            title="", 
            content=scroll, 
            size_hint=(0.7, 0.2),
            auto_dismiss=False, 
            background="", 
            separator_color=(1, 0.992, 0.815, 1),
            background_color=(1, 0.992, 0.815, 1) 
        ) 
        
        # Botón para cerrar el popup
        btn_close = Button(
            text="Cerrar", 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1, 0.992, 0.815, 1), 
            font_name="fonts/ELEPHNT", 
            bold=True, 
            font_size=20
        )
        # Caja para centrar el botón abajo 
        btn_box = BoxLayout( 
            orientation="vertical", 
            size_hint_y=None, 
            height=70, 
            padding=[0, 10, 0, 0] 
        ) 
        btn_box.add_widget(btn_close) 
        content.add_widget(btn_box) 
        btn_close.bind(on_press=lambda inst: popup.dismiss())
        
        popup.open()
        

