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
from kivy.clock import Clock
from widgets import ImageButton,RoundedButton,RoundedBox
from utils import load_events,load_resources,save_events

load_events()

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
            color=(0.251, 0.765, 0.851, 1),
            font_name="fonts/poppins-bold.ttf",
            font_size="40sp",
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

        layout = GridLayout( cols=1, spacing=10, padding=20, size_hint_y=None ) 
        layout.bind(minimum_height=layout.setter("height"))

        for idx, ev in enumerate(self.events):
            # Contenedor horizontal para cada evento
            try :
                event_date=datetime.strptime(ev["start"], "%Y-%m-%d %H:%M")
                past=event_date < datetime.now()
            except (ValueError, KeyError):
                past=False
            
            #Si el evento es anterior a la fecha actual se muestra en un rectangulo gris
            if past:
                border=(0.75, 0.75, 0.75, 1)
                background = (0.90, 0.90, 0.90, 1)
                text_color = (0.2, 0.2, 0.2, 1)
            #Si el evento no es anterior a la fecha actual se muestra en un rectangulo crema
            else:
                border = (1.0, 0.976, 0.769, 1)
                background = (1.0, 0.992, 0.906, 1)
                text_color = (0.2, 0.2, 0.2, 1)

            row = RoundedBox(
                orientation="horizontal", 
                size_hint_y=None, 
                height=100, 
                border_color=border, 
                bg_color=background
            )

            # Nombre del evento 
            lbl = Label(
                text=ev["title"],
                font_size="20sp",
                font_name="fonts/OpenSans-Bold.ttf",
                color = text_color,
                halign="left",
                valign="middle",
                size_hint_x=1,
                text_size=(None, None)
            )
            lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
            row.add_widget(lbl)

            # Botón Ver detalles 
            btn_details = RoundedButton (
                text="Ver detalles",
                font_size="16sp",
                font_name="fonts/Roboto-Medium.ttf",
                size_hint_x=None,
                size_hint_y=None,
                width=150,
                pos_hint={"center_y": 0.5},
                height=40,
                background_color=(0.251, 0.765, 0.851, 1),
                color=(1, 1, 1, 1)
            )
            btn_details.bind(on_press=lambda inst, i=idx: self.show_details(i))
            row.add_widget(btn_details)

            # Botón Eliminar
            btn_delete = RoundedButton(
                text="Eliminar",
                font_size="16sp",
                font_name="fonts/Roboto-Medium.ttf",
                size_hint_x=None,
                size_hint_y=None,
                width=150,
                pos_hint={"center_y": 0.5},
                height=40,
                background_color=(0.251, 0.765, 0.851, 1),
                color=(1, 1, 1, 1)
            )
            btn_delete.bind(on_press=lambda inst, i=idx: self.confirm_delete(i))
            row.add_widget(btn_delete)

            layout.add_widget(row)
            
        scroll.add_widget(layout)

        root.add_widget(scroll)

        # Botón para volver a la pantalla principal
        def go_back(inst):
            self.manager.transition.direction="right"
            self.manager.current="home"

        btn_back = ImageButton (
            source="images/back.png",
            size_hint=(None, None),
            size=(150, 150),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.09,"center_y": 0.09}
        )
        btn_back.bind(on_press=go_back)
        root.add_widget(btn_back)

        self.add_widget(root)

    # Función para confirmar la eliminación de un evento
    def confirm_delete(self, index):

        event = self.events[index]
        series_id = event.get("series_id", None)

        content = FloatLayout()

        #Configurar Rectangulo Redondeado de fondo
        with content.canvas.before: 
            Color(0.200, 0.200, 0.200, 1) 
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
            text="¿Desea eliminar todas las ocurrencias de este evento?",
            font_name="fonts/poppins-bold.ttf", 
            font_size="23sp", 
            color=(0.200, 0.200, 0.200, 1), 
            halign="center", 
            valign="middle", 
            size_hint=(1, None), 
            height=80, 
            pos_hint={"center_x": 0.5, "center_y": 0.75}, 
            text_size=(500, None)
        )
        content.add_widget(lbl)

        btns = BoxLayout( 
            orientation="horizontal", 
            spacing=20, 
            size_hint=(None, None), 
            size=(540, 50), 
            pos_hint={"center_x": 0.5, "center_y": 0.35} 
        )

        btn_all =RoundedButton( 
            text="Sí, todas", 
            font_size="18sp", 
            font_name="fonts/Roboto-Medium.ttf", 
            size_hint=(None, None), 
            size=(160, 45), 
            background_color=(0.6, 1, 0.6, 1), 
            color=(1,1,1,1)
        )
        btns.add_widget(btn_all)

        btn_one = RoundedButton( 
            text="No, solo esta", 
            font_size="18sp", 
            font_name="fonts/Roboto-Medium.ttf", 
            size_hint=(None, None), 
            size=(160, 45), 
            background_color=(0.251, 0.765, 0.851, 1),
            color=(1,1,1,1)
        )
        btns.add_widget(btn_one)

        btn_cancel = RoundedButton( 
            text="Cancelar", 
            font_size="18sp", 
            font_name="fonts/Roboto-Medium.ttf", 
            size_hint=(None, None), 
            size=(160, 45), 
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0.243, 0.153, 0.137, 1)
        )
        btns.add_widget(btn_cancel)
        
        content.add_widget(btns)

        popup = Popup(
            title="",
            content=content,
            size_hint=(None,None),
            auto_dismiss=False,
            size=(600,250),
            background="",
            background_color=(0,0,0,0), 
            separator_color=(0,0,0,0)
        )

        btn_all.bind(on_press=lambda inst: self.delete_series(index,series_id, popup))
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
    def delete_series(self, index, series_id, popup):
        if(series_id):
            self.events = [ev for ev in self.events if ev.get("series_id") != series_id]
        else:
            del self.events[index]
        save_events(self.events)
        popup.dismiss()
        self.on_pre_enter()

    # Función para mostrar los detalles de un evento
    def show_details(self, index):
        event = self.events[index]

        content = FloatLayout()
        with content.canvas.before: 
            Color(0.200, 0.200, 0.200, 1) # Borde oscuro
            border = RoundedRectangle(pos=content.pos, size=content.size, radius=[20]) 
            Color(1.0, 0.992, 0.906, 1) # Fondo crema
            bg = RoundedRectangle(pos=(content.x+3, content.y+3), size=(content.width-6, content.height-6), radius=[18]) 
            
        def update_rects(*args): 
            border.pos = content.pos 
            border.size = content.size 
            bg.pos = (content.x+3, content.y+2) 
            bg.size = (content.width-6, content.height-9) 
        content.bind(pos=update_rects, size=update_rects) 
        Clock.schedule_once(lambda dt: update_rects(), 0)

        # Contenedor vertical principal que organiza el título, los datos y el botón
        main_layout = BoxLayout(
            orientation="vertical",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding=[35, 25, 35, 5],
            spacing=30,
            size_hint=(1, 0.9)
        )

        #TÍTULO DESTACADO
        title_lbl = Label(
            text="Detalles del Evento",
            font_size="30sp",
            font_name="fonts/OpenSans-Bold.ttf",
            color=(0.200, 0.200, 0.200, 1),
            halign="center",
            size_hint_y=None,
            height=35
        )
        main_layout.add_widget(title_lbl)

        #SCROLLVIEW PARA LOS DETALLES
        scroll = ScrollView( 
            size_hint=(1, 0.8), 
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=8,
            bar_color=(0.200, 0.200, 0.200, 1),
            scroll_type=['bars']
        )

        start = event.get("start", "—")
        end = event.get("end", "—")
        resources = event.get("resources", [])
        recurrence = event.get("recurrence", "Ninguna")

        resources_list = "\n".join([f"      • {r}" for r in resources])
        if not resources_list:
            resources_list = "      • Ninguno asignado"

        info_text = (
            f"  [size=25]Horario[/size]\n"
            f"[font=fonts/Roboto-Medium.ttf][size=23]      Inicio:  {start}\n"
            f"      Fin:     {end}[/size][/font]\n\n"
            f"  [size=25]Recursos Asignados[/size]\n"
            f"[font=fonts/Roboto-Medium.ttf][size=23]{resources_list}[/size][/font]\n\n"
            f"  [size=25]Recurrencia[/size]\n"
            f"[font=fonts/Roboto-Medium.ttf][size=23]      {recurrence.capitalize()}[/size][/font]"
        )
        info_lbl = Label(
            text=info_text,
            font_name="fonts/OpenSans-Bold.ttf",
            color=(0.200, 0.200, 0.200, 1),
            halign="left",
            valign="top",
            markup=True,
            size_hint_y=None
        )

        info_lbl.bind(
            size=lambda inst, val: setattr(inst, "text_size", (val[0], None)),
            texture_size=lambda inst, val: setattr(inst, "height", val[1])
        )
        
        scroll.add_widget(info_lbl)
        main_layout.add_widget(scroll)

        btn_container = FloatLayout(size_hint_y=None, height=50)
        
        btn_close = RoundedButton(
            text="Cerrar",
            font_size="22sp",
            font_name="fonts/Roboto-Medium.ttf",
            size_hint=(None, None),
            size=(160, 50),
            background_color=(1.0, 0.627, 0.478, 1), 
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            color=(1, 1, 1, 1)
        )
        btn_container.add_widget(btn_close)
        main_layout.add_widget(btn_container)

        content.add_widget(main_layout)

        popup = Popup(
            title="",
            content=content,
            size_hint=(None, None),
            auto_dismiss=False,
            size=(550, 420), 
            background="",
            background_color=(0, 0, 0, 0), 
            separator_color=(0, 0, 0, 0)
        )
        btn_close.bind(on_press=lambda inst: popup.dismiss())
        popup.open()