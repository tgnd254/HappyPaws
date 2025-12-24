from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen

class ImageButton(ButtonBehavior, Image): 
    pass

class PlaceScreen(Screen):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        root = FloatLayout()
        background=Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        label = Label(text="¿Dónde quieres realizar el evento?", font_name="fonts/SHOWG.TTF", font_size="32sp",color=(0, 0.5, 0.5, 1),pos_hint={"center_x":0.5, "center_y":0.9})
        root.add_widget(label)
        places=[ ("sala_de_procedimientos"), ("sala_quirurgica"), ("sala_de_entrevistas"), ("area_de_alojamiento"), ("area_de_alimentacion"), ("area_de_bano"), ("patio_de_ejercicios"), ("exterior")] 
        x_pos = 0.3 
        for i,name in enumerate(places):
            row=i//4
            column=i%4
            x_pos=0.2+column*0.2
            y_pos=0.6 if row==0 else 0.30
            btn = ImageButton(source="images/"+name+".png",allow_stretch=False,keep_ratio=True,size_hint=(0.20, 0.20),pos_hint={"center_x":x_pos,"center_y":y_pos})
            btn.bind(on_press=lambda inst,p=name: self.go_to(p)) 
            root.add_widget(btn)
        self.add_widget(root)
    def go_to(self,place): 
        self.manager.selected_place=place
        self.manager.current="resources"
        
