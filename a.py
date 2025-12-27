import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# Función para cargar recursos desde el JSON
def cargar_recursos():
    with open("recursos.json", "r", encoding="utf-8") as f:
        return json.load(f)

class RefugioApp(App):
    def build(self):
        self.recursos = cargar_recursos()

        # Layout principal
        layout = BoxLayout(orientation='vertical')

        # Scroll con lista de botones
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Crear un botón por cada recurso de tipo Animal
        for recurso in self.recursos:
            if recurso["tipo"] == "Animal":
                btn = Button(
                    text=recurso["nombre"],
                    size_hint_y=None,
                    height=40
                )
                btn.bind(on_press=lambda instance, r=recurso: self.mostrar_detalle(r))
                grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # Área de detalle
        self.detalle = Label(text="Selecciona un animal para ver detalles")
        layout.add_widget(self.detalle)

        return layout

    def mostrar_detalle(self, recurso):
        texto = f"{recurso['nombre']} ({recurso['tipo']})\n\n"
        texto += f"Descripción: {recurso['descripcion']}\n"
        texto += f"Asociados: {', '.join(recurso['asociado'])}\n"
        texto += f"Exclusiones: {', '.join(recurso['exclusiones'])}"
        self.detalle.text = texto

if __name__ == "__main__":
    RefugioApp().run()
