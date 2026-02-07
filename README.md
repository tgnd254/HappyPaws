
# 🐾 Planificador de Eventos para Refugios Animales

**Autora:** *Estefanía Delgado Marqués*  
**Mensaje:** *Adopten!*  
**Dedicatoria:** *A mi gatito Shiro y a mi perrita Susi. Los extraño inmensamente*  

Un sistema diseñado para apoyar la organización interna de un refugio animal, donde cada recurso importa y cada decisión impacta directamente en el bienestar de los animales.  
Este proyecto facilita la planificación de actividades, garantiza el uso seguro y coherente de los recursos y contribuye a la misión más importante: **promover la adopción responsable**.

---

# 🌟 Descripción General

La aplicación permite crear, visualizar y gestionar eventos dentro de un refugio animal, considerando:

- Disponibilidad real de recursos  
- Restricciones por especie, rol o lugar  
- Validación automática de conflictos  
- Programación de eventos simples o recurrentes  
- Eliminación individual o por series  

Todo mediante una interfaz gráfica construida con **Kivy**, intuitiva y visual.

---

# 🗓️ Eventos, Recursos y Restricciones

## Eventos
Cada evento incluye:

- Título  
- Fecha y hora de inicio y fin  
- Lugar  
- Recursos necesarios  
- Recurrencia (opcional)  

El sistema valida automáticamente que los recursos estén disponibles y que no existan conflictos.

### Ejemplos de eventos
- Vacunación mensual preventiva  
- Feria de adopción  
- Aseo y limpieza del refugio  
- Entrenamiento canino  
- Rescate y traslado de animales  
- Entrevistas de adopción  

---

## Recursos
Los recursos representan personal, insumos, herramientas, animales y equipos del refugio.  
Cada recurso tiene:

- Cantidad disponible  
- Recursos asociados (co‑requisitos)  
- Exclusiones (incompatibilidades)  
- Lugares permitidos  

### Ejemplos de lógica de recursos
- **Veterinario** → asociado a Kit Médico Básico; excluye Entrenador Certificado  
- **Vacunas** → asociadas a su especie; excluyen todas las demás  
- **Voluntario de Adopciones** → asociado a Cámara Digital; excluye Voluntario normal  
- **Carpa de Exhibición** → asociada a Voluntario y Folletos; excluye Veterinario  
- **Vehículo Petmóvil** → asociado a Voluntario; excluye Personal de Recepción  

---

## 🔒 Restricciones del Sistema

### ✔️ Co‑requisitos
Un recurso requiere otro para funcionar.  
Ejemplos:

- Vacuna Séxtuple Canina → Veterinario + Perros  
- Cámara Digital → Voluntario de Adopciones  
- Entrenador Certificado → Juguetes Interactivos  

### ❌ Exclusiones
Dos recursos no pueden coexistir en el mismo evento.  
Ejemplos:

- Veterinario ❌ Entrenador Certificado  
- Voluntario ❌ Voluntario de Adopciones  
- Vacuna Felina ❌ Perros  
- Carpa de Exhibición ❌ Veterinario  

---

# ⚙️ Funcionalidades Principales

### 🏠 Pantalla de Inicio
- Crear un nuevo evento  
- Ver eventos creados  

### 📍 Selección del Lugar
El usuario elige dónde ocurrirá el evento.

### 🧰 Selección de Recursos
El usuario selecciona los recursos necesarios.  
Se aplican reglas de asociados y exclusiones.

### ⏰ Fecha y Hora
El sistema valida:

- Disponibilidad  
- Solapamientos  
- Exclusiones  
- Asociaciones obligatorias  

Si hay conflicto, se sugiere un horario alternativo.

### 🔁 Recurrencia
Eventos diarios, semanales o mensuales.  
Cada ocurrencia se valida individualmente.

### 📋 Listado de Eventos
Tarjetas visuales con:

- Título  
- Imagen del lugar  
- Detalles  
- Eliminación  

### 🗑️ Eliminación Inteligente
- Eliminar solo una ocurrencia  
- O toda la serie  

### 🔎 Detalles del Evento
Incluye:

- Inicio y fin  
- Recursos  
- Recurrencia  
- Lugar  
- Identificador de serie  

### 💾 Persistencia
Datos guardados en:

- `data/events.json`  
- `data/resources.json`  

---

# 🖼️ Guía de la Interfaz

### Pantalla de Inicio
Botones grandes y visuales para crear o ver eventos.

### Pantalla de Lugar
Grid con imágenes de cada área del refugio.

### Pantalla de Recursos
Lista de recursos seleccionables.

### Pantalla de Fecha y Hora
Validación automática y mensajes claros.

### Pantalla de Recurrencia
Configuración de patrones repetitivos.

### Pantalla de Eventos Creados
Tarjetas con detalles y opciones de eliminación.

---

# 🌳 Árbol de Directorios

```txt
Planificador-de-Eventos/
├── data/
│   ├── events.json
│   └── resources.json
│
├── fonts/
│   └── (tipografías .ttf usadas en la interfaz)
│
├── images/
│   └── (iconos, fondos, botones, go_back, check, etc.)
│
├── .gitignore
├── requirements.txt
│
├── main.py
├── place.py
├── resources.py
├── date.py
├── recurrence.py
├── events.py
│
├── utils.py        ← funciones de lógica y manejo de datos
└── widgets.py      ← widgets personalizados (RoundedButton, ImageButton, etc.)

```


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
