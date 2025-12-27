from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

class ImageButton(ButtonBehavior, Image): 
    pass

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root=FloatLayout()
        background=Image(source="refugio.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        button_crear_evento = ImageButton(source="crear_evento.png", size_hint=(0.2, 0.3),pos_hint={"center_x":0.1, "center_y":0.8})
        button_crear_evento.bind(on_press=self.on_image_click) 
        root.add_widget(button_crear_evento)
        self.add_widget(root)
    def on_image_click(self, instance): 
        self.manager.current = "second"
class SecondScreen(Screen): 
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        root = FloatLayout() 
        background = Image(source="otra_imagen.png", allow_stretch=True, keep_ratio=False) 
        root.add_widget(background) 
        self.add_widget(root) 
class FirstWindow(App): 
    def build(self): 
        sm = ScreenManager() 
        sm.add_widget(FirstScreen(name="first")) 
        sm.add_widget(SecondScreen(name="second")) 
        return sm
        
                               
if __name__ == "__main__":
    FirstWindow().run()