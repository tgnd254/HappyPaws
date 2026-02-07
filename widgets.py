# widgets.py
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.label import Label 
from kivy.uix.scrollview import ScrollView 
from kivy.uix.popup import Popup 
from kivy.clock import Clock

# Botón con imagen 
class ImageButton(ButtonBehavior, Image):
    pass

# Botón redondeado
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.bg_color = kwargs.get("background_color", (0.251, 0.765, 0.851, 1))
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Caja redondeada 
class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 10
        self.spacing = 10

        with self.canvas.before:
            Color(1.0, 0.976, 0.769, 1)
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            Color(1.0, 0.992, 0.906, 1)
            self.bg = RoundedRectangle(pos=(self.x+3, self.y+3),
                                       size=(self.width-6, self.height-6),
                                       radius=[10])
        self.bind(pos=self.update_rects, size=self.update_rects)

    def update_rects(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size
        self.bg.pos = (self.x+3, self.y+3)
        self.bg.size = (self.width-6, self.height-6)

# Metodo para mostrar mensajes de error en pantalla
def show_message(text, color=(0.243, 0.153, 0.137, 1)):
    content = FloatLayout()
    with content.canvas.before:
        Color(1.0, 0.627, 0.478, 1)
        border = RoundedRectangle(pos=content.pos, size=content.size, radius=[20])
        Color(1.0, 0.992, 0.906, 1)
        bg = RoundedRectangle(pos=(content.x+3, content.y+3),
                              size=(content.width-6, content.height-6),
                              radius=[18])

    def update_rects(*args):
        border.pos = content.pos
        border.size = content.size
        bg.pos = (content.x+3, content.y+3)
        bg.size = (content.width-6, content.height-6)

    content.bind(pos=update_rects, size=update_rects)
    Clock.schedule_once(lambda dt: update_rects(), 0)

    scroll = ScrollView(
        size_hint=(1, 0.6),
        pos_hint={"center_x": 0.5, "center_y": 0.65},
        do_scroll_x=False,
        do_scroll_y=True,
        bar_width=12,
        bar_color=(0.251, 0.765, 0.851, 1),
        scroll_type=['bars']
    )

    lbl = Label(
        text=text,
        font_size="22sp",
        font_name="fonts/OpenSans-Bold.ttf",
        color=color,
        halign="center",
        valign="middle",
        size_hint=(1, None),
        text_size=(500, None)
    )
    lbl.bind(texture_size=lambda inst, val: setattr(lbl, "height", val[1]))
    scroll.add_widget(lbl)
    content.add_widget(scroll)

    # Botón cerrar
    btn_close = RoundedButton(
        text="Cerrar",
        font_size="18sp",
        font_name="fonts/Roboto-Medium.ttf",
        background_color=(1.0, 0.627, 0.478, 1),
        size_hint=(None, None),
        size=(160, 45),
        pos_hint={"center_x": 0.5, "center_y": 0.2},
        color=(1, 1, 1, 1)
    )
    content.add_widget(btn_close)

    popup = Popup(
        title="",
        content=content,
        size_hint=(None, None),
        auto_dismiss=False,
        size=(600, 230),
        background="",
        background_color=(0, 0, 0, 0),
        separator_color=(0, 0, 0, 0)
    )
    btn_close.bind(on_press=lambda inst: popup.dismiss())
    popup.open()
