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

class ImageButton(ButtonBehavior, Image):
    pass

class ResourcesScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Cargar recursos desde JSON
        with open("resources.json", "r", encoding="utf-8") as f:
            self.resources = json.load(f)
        self.selected_resources = []
        self.buttons = {}

    def validate_resources(self):
        errors = []
        for r in self.resources:
            name = r["name"]
            if name in self.selected_resources:
                for excl in r.get("exclusions", []):
                    if excl in self.selected_resources:
                        errors.append(f"{name} no puede usarse junto a {excl}")
                for assoc in r.get("associated", []):
                    if assoc not in self.selected_resources:
                        errors.append(f"{name} requiere {assoc}")
        return errors

    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()
        background = Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        label = Label(
            text="Selecciona los recursos necesarios para tu evento",
            color=(0, 0.5, 0.5, 1),
            font_name="fonts/SHOWG.TTF",
            font_size="28sp",
            pos_hint={"center_x": 0.5, "center_y": 0.95}
        )
        root.add_widget(label)

        scroll = ScrollView(
            size_hint=(1, 0.65),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=12,
            bar_margin=8,
            bar_color=(0, 0.7, 0.7, 1),
            scroll_type=['bars']
        )
        grid = GridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        place = self.manager.selected_place
        place_resources = [r for r in self.resources if place in r["place"]]

        # Crear cada fila de recurso
        for r in place_resources:
            card = BoxLayout(
                orientation="horizontal",
                height=170,
                spacing=40,
                size_hint=(1, None),
                padding=(10,10)
            )
            with card.canvas.before:
                Color(0.6, 1, 0.6, 1) 
                rr = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
            def update_rr(instance,value,rect=rr,widget=card): 
                rect.pos = (widget.x+5 ,widget.y+5) 
                rect.size = (widget.width-10,widget.height-10)
            card.bind(pos=update_rr, size=update_rr) 
            Clock.schedule_once(lambda dt: update_rr(card,None), 0)

            btn = ImageButton(
                source="images/" + r["name"] + ".png",
                size_hint=(None, None),
                size=(150, 150),
                allow_stretch=True,
                keep_ratio=True
            )
            btn.resource = r
            btn.bind(on_press=lambda inst, res=r: self.toggle_resource(res))

            info_box = BoxLayout(orientation="vertical", spacing=0,padding=(10,10))

            name_label = Label(
                text=r["name"],
                font_size="18sp",
                bold=True,
                color=(0.2078, 0.4980, 0.7294, 1),
                halign="left",
                valign="bottom",
                size_hint_y=None,
                height=25, 
            )
        
            name_label.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))

            desc_label = Label(
                text=r.get("description", ""),
                font_size="16sp",
                color=(0.2078, 0.4980, 0.7294, 1),
                halign="left",
                valign="top",
                height=40
            )
            desc_label.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))

            info_box.add_widget(name_label)
            info_box.add_widget(desc_label)

            card.add_widget(btn)
            card.add_widget(info_box) 
            grid.add_widget(card)
            self.buttons[r["name"]] = btn

        scroll.add_widget(grid)
        root.add_widget(scroll)

        self.msg_label = Label(
            text="Seleccionados:",
            font_size="20sp",
            pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        root.add_widget(self.msg_label)

        btn_continue = Button(
            text="Continuar",
            size_hint=(0.2, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            background_color=(0, 0.5, 0.5, 1)
        )
        btn_continue.bind(on_press=self.try_continue)
        root.add_widget(btn_continue)

        def go_back(inst):
            self.manager.current="place"

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

    def toggle_resource(self, resource):
        name = resource["name"]
        if name not in self.selected_resources:
            self.selected_resources.append(name)
            self.buttons[name].color = (0, 0, 1, 1)
        else:
            self.selected_resources.remove(name)
            self.buttons[name].color = (1, 1, 1, 1)

        errors = self.validate_resources()
        if errors:
            self.msg_label.text = "\n".join(errors)
        else:
            self.msg_label.text = f"Seleccionados: {', '.join(self.selected_resources)}"

    def try_continue(self, instance):
        errors = self.validate_resources()
        if errors:
            self.msg_label.text = "\n".join(errors)
            return
        self.manager.selected_resources = self.selected_resources
        self.manager.current = "date"
