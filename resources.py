import json
from kivy.uix.screenmanager import Screen 
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.label import Label 
from kivy.uix.image import Image 
from kivy.uix.behaviors import ButtonBehavior 

class ImageButton(ButtonBehavior, Image): 
    pass

class ResourcesScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        with open("recursos.json","r",encoding="utf-8") as f: 
            self.resources = json.load(f) 
        self.selected_resources = [] 
        self.buttons = {}
    def on_pre_enter(self): 
        self.clear_widgets() 
        root = FloatLayout() 
        place = self.manager.selected_place 
        #place_resources = [r for r in self.resources if r["place"] == place]
        background=Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        label = Label(text=f"Selecciona los recursos necesarios para tu evento",color=(0, 0.5, 0.5, 1),font_name="fonts/SHOWG.TTF",font_size="28sp",pos_hint={"center_x":0.5,"center_y":0.9}) 
        root.add_widget(label)
        self.add_widget(root)

