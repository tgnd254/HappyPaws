# 🐾 Planificador de Eventos para Refugios Animales

Un sistema pensado para facilitar la organización interna de un refugio animal. Cada recurso importa: la aplicación ayuda a planificar actividades, validar disponibilidad y prevenir conflictos, favoreciendo así el bienestar animal y la adopción responsable.

---

## Índice

- [Descripción](#descripción)
- [Características principales](#características-principales)
- [Eventos, recursos y restricciones](#eventos-recursos-y-restricciones)
- [Interfaz (guía rápida)](#interfaz-guía-rápida)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Dependencias](#dependencias)
- [Autor y dedicatoria](#autor-y-dedicatoria)

---

## Descripción

La aplicación permite crear, visualizar y gestionar eventos en un refugio animal teniendo en cuenta:

- Disponibilidad real de recursos (personas, insumos, equipamiento, animales).
- Reglas de co‑requisitos y exclusiones entre recursos.
- Validación de solapamientos y disponibilidad por cantidad.
- Creación de eventos simples y recurrentes (serie de eventos).

Todo esto mediante una interfaz gráfica construida con Kivy, diseñada para ser clara e intuitiva.

---

## Características principales

1. Crear eventos con título, lugar, recursos y ventana de tiempo.
2. Validación automática de conflictos (recursos, fechas, exclusiones).
3. Programación de recurrencias: diarias, semanales y mensuales.
4. Eliminación inteligente: instancia única o toda la serie.
5. Persistencia en archivos JSON: `data/events.json` y `data/resources.json`.
6. Gestión visual de recursos (cantidades, asociados y exclusiones).

---

## Eventos, recursos y restricciones

### Eventos
Cada evento incluye:

- Título
- Fecha y hora de inicio y fin
- Lugar
- Recursos necesarios
- Recurrencia (opcional)

### Recursos
Los recursos representan personal, insumos, herramientas, animales y equipos.
Se definen con:

- Cantidad disponible
- Recursos asociados (co‑requisitos)
- Exclusiones (incompatibilidades)
- Lugares permitidos

Ejemplos:
- Veterinario (asocia: Kit Médico Básico; excluye: Entrenador Certificado)
- Vacuna (asociada a especie y veterinario)
- Voluntario de Adopciones (asocia: Cámara Digital; excluye: Voluntario normal)

---

## Interfaz (guía rápida)

- Pantalla principal: Crear evento / Ver eventos creados.
- Selección de lugar: grid con imágenes por área.
- Selección de recursos: lista con selección múltiple y validaciones.
- Fecha y hora: campos para inicio/fin y validación en tiempo real.
- Recurrencia: popup para configurar tipo y límite de fechas.
- Listado de eventos: tarjetas con botones de detalles y eliminación.

---

## Estructura del proyecto

Planificador-de-Eventos/

```
├── data/
│   ├── events.json
│   └── resources.json
├── fonts/
│   └── (tipografías .ttf usadas en la interfaz)
├── images/
│   └── (iconos, fondos y botones de la aplicación)
├── .gitignore
├── requirements.txt
├── main.py
├── place.py
├── resources.py
├── date.py
├── recurrence.py
└── events.py
```

---

## Instalación y ejecución

Sigue estos pasos según tu sistema operativo. Se asume que tienes Python instalado.

1) Clonar el repositorio

```bash
git clone https://github.com/tuusuario/Planificador-de-Eventos.git
cd Planificador-de-Eventos
```

2) Crear y activar un entorno virtual

- Windows (PowerShell):

```powershell
python -m venv venv
# Si tu política de ejecución no permite scripts, usa:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

- Windows (sí usas cmd.exe):

```cmd
python -m venv venv
venv\Scripts\activate
```

- Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

3) Instalar dependencias

```bash
pip install -r requirements.txt
```

4) Ejecutar la aplicación

```bash
python main.py
```

---

## Dependencias

Las dependencias principales están en `requirements.txt`. La aplicación se desarrolló con Kivy como dependencia central.

---

## Uso rápido

- Crear evento → completar título, lugar, recursos y rango horario.
- Si el recurso tiene co‑requisitos o exclusiones, el sistema los aplicará al seleccionar.
- Para recurrencia, usar la opción de recurrencia y definir la serie; cada instancia se valida por separado.
- Para eliminar, abrir detalles y elegir eliminar sólo la ocurrencia o la serie completa.

---

## Autor y dedicatoria

Autora: Estefanía Delgado Marqués

¡Adopten! 🐶🐱

Dedicatoria: A mi gatito Shiro — te extraño inmensamente.

---

Si quieres que ajuste el tono, el idioma o añada ejemplos visuales (capturas o GIF), indícalo y lo incorporo antes de hacer el commit final del README.