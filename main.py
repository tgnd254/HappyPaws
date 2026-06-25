
from kivy.config import Config 

# Bloquear redimensionamiento 
Config.set('graphics', 'resizable', False) 
# Definir tamaño fijo de la ventana 
Config.set('graphics', 'width', '800') 
Config.set('graphics', 'height', '600')
# Desactivar el puntico rojo de clic derecho
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Heredamos de MDApp para poder usar el calendario y reloj
from kivymd.app import MDApp

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from widgets import ImageButton

from screens import PlaceScreen, ResourcesScreen, DateScreen, EventsScreen, RecurrenceScreen

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root=FloatLayout()
        background=Image(source="images/refugio.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

       #Botón para crear eventos
        button_make_event = ImageButton(
            source="images/crear_evento.png", 
            size_hint=(0.3, 0.3),
            pos_hint={"center_x":0.13, "center_y":0.85}  
        )

        #Botón para ver eventos creados
        button_created_events = ImageButton(
            source="images/eventos_creados.png", 
            size_hint=(0.3, 0.3),
            pos_hint={"center_x":0.13, "center_y":0.6}
        )

        button_created_events.bind(on_press=self.go_to_events)
        button_make_event.bind(on_press=self.go_to_place) 

        root.add_widget(button_make_event)
        root.add_widget(button_created_events)
        self.add_widget(root)

    #Funcion para ir a la pantalla de seleccionar lugar
    def go_to_place(self, instance): 
        self.manager.current = "place"
        self.manager.transition.direction= "left"

    #Funcion para ir a la pantalla donde se muestran los eventos
    def go_to_events(self,instance):
        self.manager.current="events"
        self.manager.transition.direction= "left"


class HappyPaws(MDApp): 

    def build(self): 
        #Modificar tema del calendario y reloj
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan" 

        sm = ScreenManager()
        sm.selected_place = None

        #Añadir transicion entre pantallas
        sm.transition = SlideTransition(duration=0.3)
        
        #Añadir pantallas al gestor de pantallas
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaceScreen(name="place"))
        sm.add_widget(ResourcesScreen(name="resources"))
        sm.add_widget(DateScreen(name="date"))
        sm.add_widget(EventsScreen(name="events"))
        sm.add_widget(RecurrenceScreen(name="recurrence"))
        sm.current="home"
        return sm
                                
if __name__ == "__main__":
    HappyPaws().run()