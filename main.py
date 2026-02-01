from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from place import PlaceScreen
from resources import ResourcesScreen
from date import DateScreen

class ImageButton(ButtonBehavior, Image): 
    pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root=FloatLayout()
        background=Image(source="images/refugio.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        button_crear_evento = ImageButton(source="images/crear_evento.png", size_hint=(0.2, 0.3),pos_hint={"center_x":0.1, "center_y":0.8})
        button_crear_evento.bind(on_press=self.go_to_place) 
        root.add_widget(button_crear_evento)
        self.add_widget(root)
    def go_to_place(self, instance): 
        self.manager.current = "place"

class FirstWindow(App): 
    def build(self): 
        sm = ScreenManager() 
        sm.selected_place = None
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaceScreen(name="place"))
        sm.add_widget(ResourcesScreen(name="resources"))
        sm.add_widget(DateScreen(name="date"))
        sm.current="home"
        return sm
        
                               
if __name__ == "__main__":
    FirstWindow().run()