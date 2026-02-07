import json
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from widgets import ImageButton,RoundedButton,show_message
from utils import load_events,load_resources,save_events,validate_resources

class ResourcesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.resources = load_resources()

        self.selected_resources = []
        self.buttons = {}
    
    def on_pre_enter(self):
        # Limpiar widgets anteriores
        self.clear_widgets()

        root = FloatLayout()

        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        label = Label(
            text="Selecciona los recursos necesarios para tu evento",
            color=(0.251, 0.765, 0.851, 1), 
            font_name="fonts/poppins-bold.ttf", 
            font_size="30sp", 
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        )
        root.add_widget(label)

        # Crear scroll para los recursos
        scroll_resources = ScrollView(
            size_hint=(0.95, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=12,
            bar_color=(0.251, 0.765, 0.851, 1),
            scroll_type=['bars']
        )

        grid = GridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        place = self.manager.selected_place
        place_resources = [r for r in self.resources if place in r["place"]]

        # Crear cada fila de recurso
        for r in place_resources:
            # Crear tarjeta para el recurso
            card = BoxLayout(
                orientation="horizontal",
                height=180,
                spacing=20,
                size_hint=(1, None),
                padding=15
            )
            # Crear fondo redondeado
            with card.canvas.before:
                Color(1.0, 0.976, 0.769, 1)
                border = RoundedRectangle(pos=card.pos, size=card.size, radius=[15])
                Color(1.0, 0.992, 0.906, 1)   
                bg = RoundedRectangle(pos=(card.x+3, card.y+3), size=(card.width-6, card.height-6), radius=[12])
            def update_card(instance, value, b=border, g=bg, widget=card): 
                b.pos = widget.pos 
                b.size = widget.size 
                g.pos = (widget.x+3, widget.y+3) 
                g.size = (widget.width-6, widget.height-6)
            card.bind(pos=update_card, size=update_card)
            Clock.schedule_once(lambda dt: update_card(card,None), 0)
            
            # Mostrar imagen de los recursos
            btn = ImageButton(
                source="images/" + r["name"].lower().replace(" ", "_")+ ".png",
                mipmap=True,
                size_hint=(None, None),
                size=(150, 150),
                allow_stretch=False,
                keep_ratio=True
            )
            btn.resource = r
            btn.bind(on_press=lambda inst, res=r: self.toggle_resource(res))

            # Mostrar nombre y descripcion de los recursos
            info_box = BoxLayout(orientation="vertical", spacing=8 ,padding=(5,10))

            name_label = Label(
                text=r["name"],
                font_size="22sp",
                font_name="fonts/OpenSans-Bold.ttf",
                color=(0.251, 0.765, 0.851, 1),
                halign="left",
                valign="bottom",
                size_hint_y=None,
                height=25, 
            )
            name_label.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))

            desc_label = Label(
                text=r.get("description", ""),
                font_size="20sp",
                font_name="fonts/Roboto-Medium.ttf",
                color=(0.243, 0.153, 0.137, 1),
                halign="left",
                valign="top",
                size_hint_y=None,
                height=60
            )
            desc_label.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))

            info_box.add_widget(name_label)
            info_box.add_widget(desc_label)

            card.add_widget(btn)
            card.add_widget(info_box) 

            grid.add_widget(card)

            self.buttons[r["name"]] = btn

        scroll_resources.add_widget(grid)
        root.add_widget(scroll_resources)

        # Botón para continuar
        btn_continue = ImageButton(
            source="images/check..png",
            size_hint=(None, None),
            pos_hint={"center_x": 0.90, "center_y": 0.09},
            size=(150,150),
            allow_stretch=True,
            keep_ratio=True,
        )
        btn_continue.bind(on_press=self.try_continue)
        root.add_widget(btn_continue)

        # Botón para volver
        def go_back(inst):
            self.manager.current="place"

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

    # Método para la selección de recursos
    def toggle_resource(self, resource):
        name = resource["name"]
        # Si el recurso esta seleccionado se muestra en azul
        if name not in self.selected_resources:
            self.selected_resources.append(name)
            self.buttons[name].color = (0.5, 0.7, 1, 1)
        # Si el recurso no está seleccionado se muestra en blanco
        else:
            self.selected_resources.remove(name)
            self.buttons[name].color = (1, 1, 1, 1)

    # Método para continuar. Verificar si no quedan errores
    def try_continue(self, instance):
        errors = validate_resources(self.resources,self.selected_resources)
        if errors:
            show_message(errors[0])
            return
        
        self.manager.selected_resources = self.selected_resources
        self.manager.current = "date"
