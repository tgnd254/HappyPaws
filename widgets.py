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
from kivy.core.audio import SoundLoader

def play_sound(file="sounds/click.mp3"): 
    click_sound=SoundLoader.load(file)
    if click_sound: 
        click_sound.play()


# Botón con imagen 
class ImageButton(ButtonBehavior, Image):
    def __init__(self, sound_file="sounds/click.mp3", **kwargs): 
        super().__init__(**kwargs) 
        self.sound_file = sound_file 
        self.is_selected= False
        self.bind(on_press=self._play_sound) 
        
    #Reproducir sonido al hacer clic
    def _play_sound(self, *args): 
        play_sound(self.sound_file)

    # Cambiar color al presionar
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.color = (0.6, 0.6, 0.6, 1)
            
        return super().on_touch_down(touch)

    # Cambiar color al soltar
    def on_touch_up(self, touch):
        if self.is_selected:
            self.color=(0.5,0.7,1,1)
        else:
            self.color = (1, 1, 1, 1)
        
        return super().on_touch_up(touch)

# Botón redondeado
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""

        self.original_color = kwargs.get("background_color", (0.251, 0.765, 0.851, 1))
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            self.canvas_color=Color(*self.original_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.bind(on_press=self._play_sound) 

    def _play_sound(self, *args):
        play_sound()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            dark_color = (self.original_color[0] * 0.7, 
                          self.original_color[1] * 0.7, 
                          self.original_color[2] * 0.7, 
                          self.original_color[3])

            self.canvas_color.rgba = dark_color  

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.canvas_color.rgba = self.original_color
        
        return super().on_touch_up(touch)

# Caja redondeada 
class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
    
        self.border_color=kwargs.pop("border_color", (1.0, 0.976, 0.769, 1))
        self.bg_color = kwargs.pop("bg_color", (1.0, 0.992, 0.906, 1))

        super().__init__(**kwargs)
        
        self.padding = 10
        self.spacing = 10

        with self.canvas.before:
            self.canvas_border_color = Color(*self.border_color)
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            self.canvas_bg_color = Color(*self.bg_color)
            self.bg = RoundedRectangle(
                pos=(self.x+3, self.y+3),
                size=(self.width-6, self.height-6),
                radius=[10]
            )
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
        bg = RoundedRectangle(
            pos=(content.x+3, content.y+3),
            size=(content.width-6, content.height-6),
            radius=[18]
        )

    def update_rects(*args):
        border.pos = content.pos
        border.size = content.size
        bg.pos = (content.x+3, content.y+3)
        bg.size = (content.width-6, content.height-6)

    content.bind(pos=update_rects, size=update_rects)
    Clock.schedule_once(lambda dt: update_rects(), 0)

    scroll = ScrollView(
        size_hint=(0.9, 0.65),
        pos_hint={"center_x": 0.5, "center_y": 0.65},
        do_scroll_x=False,
        do_scroll_y=True,
        bar_width=10,
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
        pos_hint={"center_x": 0.5, "center_y": 0.15},
        color=(1, 1, 1, 1)
    )
    content.add_widget(btn_close)

    popup = Popup(
        title="",
        content=content,
        size_hint=(None, None),
        auto_dismiss=False,
        size=(600, 260),
        background="",
        background_color=(0, 0, 0, 0),
        separator_color=(0, 0, 0, 0)
    )
    btn_close.bind(on_press=lambda inst: popup.dismiss())
    popup.open()

#Metodo para mostrar mensaje de cargando
def show_loading(text="Cargando recursos...", color=(0.243, 0.153, 0.137, 1)):
    content = FloatLayout()
    with content.canvas.before:
        Color(1.0, 0.627, 0.478, 1)  
        border = RoundedRectangle(pos=content.pos, size=content.size, radius=[20])
        Color(1.0, 0.992, 0.906, 1) 
        bg = RoundedRectangle(
            pos=(content.x+3, content.y+3),
            size=(content.width-6, content.height-6),
            radius=[18]
        )

    def update_rects(*args):
        border.pos = content.pos
        border.size = content.size
        bg.pos = (content.x+3, content.y+3)
        bg.size = (content.width-6, content.height-6)

    content.bind(pos=update_rects, size=update_rects)
    Clock.schedule_once(lambda dt: update_rects(), 0)

    lbl = Label(
        text=text,
        font_size="30sp",
        font_name="fonts/OpenSans-Bold.ttf",
        color=color,
        halign="center",
        valign="middle",
        size_hint=(1, 1),
        pos_hint={"center_x": 0.5, "center_y": 0.5},
        text_size=(500, None)
    )
    content.add_widget(lbl)

    popup = Popup(
        title="",
        content=content,
        size_hint=(None, None),
        auto_dismiss=False,
        size=(600, 200),
        background="",
        background_color=(0, 0, 0, 0),
        separator_color=(0, 0, 0, 0)
    )
    popup.open()
    return popup

