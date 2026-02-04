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

    #Crear la interfaz de usuario
    def on_pre_enter(self, *args):
        
        root = FloatLayout()

        background=Image(source="images/background.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        label = Label(text="¿Dónde quieres realizar el evento?", font_name="fonts/SHOWG.TTF", font_size="32sp",color=(0, 0.5, 0.5, 1),pos_hint={"center_x":0.5, "center_y":0.9})
        root.add_widget(label)

        places=[ 
            ("sala_de_procedimientos"), 
            ("sala_quirúrgica"), 
            ("sala_de_entrevistas"), 
            ("área_de_alojamiento"), 
            ("área_de_alimentacion"), 
            ("área_de_bano"), 
            ("patio_de_ejercicios"), 
            ("exterior")
        ] 

        #Crear botones para cada lugar
        x_pos = 0.3 
        for i,name in enumerate(places):
            row=i//4
            column=i%4
            x_pos=0.2+column*0.2
            y_pos=0.6 if row==0 else 0.30
            btn = ImageButton(
                source="images/"+name+".png",
                allow_stretch=False,
                keep_ratio=True,
                size_hint=(0.20, 0.20),
                pos_hint={"center_x":x_pos,"center_y":y_pos}
            )
            btn.bind(on_press=lambda inst, p=name: self.go_to(p))
            root.add_widget(btn)

        # Crear botón de retroceso
        def go_back(inst):
            self.manager.current="home"

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

    # Método para cambiar a la pantalla de recursos
    def go_to(self,place):
        self.manager.selected_place=place
        self.manager.current="resources"
        
