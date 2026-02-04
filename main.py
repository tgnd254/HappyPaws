# Planificador de Eventos - Interfaz principal
# Archivo: main.py
# Contiene: definición de pantallas principales y gestor de pantallas

# --- Imports ---
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Importar pantallas definidas en módulos locales
from place import PlaceScreen
from resources import ResourcesScreen
from date import DateScreen
from events import EventsScreen
from recurrence import RecurrenceScreen


# --- Widgets auxiliares ---
class ImageButton(ButtonBehavior, Image):
    """Botón que utiliza una imagen como fondo.
    Hereda de ButtonBehavior para detectar eventos y de Image para mostrar la imagen.
    """
    pass


# --- Pantalla de inicio ---
class HomeScreen(Screen):
    """Pantalla principal (home) con acceso a creación de eventos y listado de eventos.
    Se construye manualmente con FloatLayout e imágenes como botones.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        # Imagen de fondo (cubre toda la pantalla)
        background = Image(source="images/refugio.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(background)

        # Botones principales: crear evento y ver eventos creados
        button_crear_evento = ImageButton(
            source="images/crear_evento.png",
            size_hint=(0.2, 0.3),
            pos_hint={"center_x": 0.1, "center_y": 0.8}
        )
        button_eventos_creados = ImageButton(
            source="images/eventos_creados.png",
            size_hint=(0.2, 0.3),
            pos_hint={"center_x": 0.1, "center_y": 0.6}
        )

        # Vincular eventos de los botones a funciones de navegación
        button_eventos_creados.bind(on_press=self.go_to_events)
        button_crear_evento.bind(on_press=self.go_to_place)

        # Añadir widgets al layout
        root.add_widget(button_crear_evento)
        root.add_widget(button_eventos_creados)

        self.add_widget(root)

    # --- Funciones de navegación ---
    def go_to_place(self, instance):
        """Ir a la pantalla de selección de lugar."""
        self.manager.current = "place"

    def go_to_events(self, instance):
        """Ir a la pantalla de eventos creados."""
        self.manager.current = "events"


# --- Clase principal de la aplicación ---
class FirstWindow(App):
    """Clase principal de la aplicación Kivy.
    Construye el ScreenManager y registra todas las pantallas usadas.
    """
    def build(self):
        # Crear el gestor de pantallas
        sm = ScreenManager()

        # Propiedad auxiliar para comunicar la selección de lugar
        sm.selected_place = None

        # Registrar pantallas en el ScreenManager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaceScreen(name="place"))
        sm.add_widget(ResourcesScreen(name="resources"))
        sm.add_widget(DateScreen(name="date"))
        sm.add_widget(EventsScreen(name="events"))
        sm.add_widget(RecurrenceScreen(name="recurrence"))

        # Pantalla inicial
        sm.current = "home"
        return sm


# Punto de entrada
if __name__ == "__main__":
    FirstWindow().run()