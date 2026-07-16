
# 🐾 Planificador de Eventos para Refugios Animales

**Autora:** *Estefanía Delgado Marqués*  
**Mensaje:** *¡Adopten!*  
**Dedicatoria:** *A mi gatito Shiro y a mi perrita Susi. Los extraño inmensamente.*

Un sistema diseñado para apoyar la organización interna de un refugio animal, donde cada recurso importa y cada decisión impacta directamente en el bienestar de los animales. Este proyecto facilita la planificación de actividades, garantiza el uso seguro y coherente de los recursos, y contribuye a la misión más importante: **promover la adopción responsable**.

---

## 🌟 Descripción General y Motivación del Dominio

La elección de un refugio animal como dominio no fue arbitraria. Los refugios son entornos donde la coordinación de recursos es crítica: un veterinario no puede estar en dos procedimientos a la vez, una vacuna canina no puede administrarse en presencia de gatos, y una feria de adopción requiere voluntarios, carpa y folletos funcionando en conjunto. Cualquier fallo en esa coordinación no es solo un problema logístico, sino que puede poner en riesgo la salud de los animales o la calidad del proceso de adopción.

El planificador resuelve exactamente ese problema: garantiza que ningún recurso se asigne a dos eventos simultáneos, que las combinaciones de recursos sean siempre coherentes con las reglas del refugio, y que cuando un horario no esté disponible, el sistema sugiera automáticamente el siguiente hueco libre.

La aplicación permite crear, visualizar y gestionar eventos considerando:

- Disponibilidad real de recursos con cantidades múltiples
- Restricciones por especie, rol o lugar
- Validación automática de conflictos mediante un algoritmo de barrido temporal (sweep line)
- Programación de eventos simples o recurrentes (diaria, semanal, mensual)
- Eliminación individual o por series completas
- Persistencia total del estado en archivos JSON

Todo mediante una interfaz gráfica construida con **Kivy** y **KivyMD**, intuitiva, visual y con efectos de sonido para cada especie animal.

---

## 🗓️ Modelo del Dominio: Eventos

Un evento representa cualquier actividad planificada dentro del refugio que requiere recursos específicos durante un intervalo de tiempo determinado. Cada evento almacena:

- **Título:** nombre descriptivo de la actividad
- **Lugar:** el área del refugio donde se realizará
- **Recursos asignados:** lista de recursos necesarios para llevarlo a cabo
- **Fecha y hora de inicio y fin:** el intervalo temporal reservado
- **Recurrencia:** patrón de repetición, si aplica (diaria, semanal, mensual)
- **Identificador de serie:** UUID único que agrupa todas las ocurrencias de un evento recurrente

### Ejemplos de eventos reales en el refugio

| Evento | Lugar | Duración típica |
|---|---|---|
| Vacunación mensual preventiva | Sala de procedimientos | 2–4 horas |
| Feria de adopción | Exterior | 4–6 horas |
| Aseo y limpieza general | Área de alojamiento | 1–2 horas |
| Entrenamiento canino | Patio de ejercicios | 1 hora |
| Rescate y traslado de animales | Exterior | Variable |
| Entrevista de adopción | Sala de entrevistas | 30–60 min |
| Cirugía de esterilización | Sala quirúrgica | 1–3 horas |
| Alimentación grupal | Área de alimentación | 30 min |
| Baño e higiene | Área de baño | 1–2 horas |

---

## 🧰 Modelo del Dominio: Recursos

Los recursos representan todos los activos finitos del refugio: personal, insumos médicos, herramientas, animales y equipos. Cada recurso está definido por los siguientes atributos en `resources.json`:

```json
{
  "name": "Veterinario",
  "place": ["sala_de_procedimientos", "sala_quirúrgica"],
  "description": "Profesional encargado de la salud animal.",
  "associated": ["Kit Médico Básico"],
  "exclusions": ["Entrenador Certificado", "Voluntarios Paseadores"],
  "quantity": 2
}
```

- **name:** identificador único del recurso
- **place:** lista de lugares donde puede ser utilizado
- **description:** descripción funcional del recurso
- **associated:** recursos que deben acompañarlo obligatoriamente (co-requisitos)
- **exclusions:** recursos con los que es incompatible en el mismo evento
- **quantity:** número de unidades disponibles simultáneamente

### Categorías de recursos del refugio

**Personal:**
Veterinario, Voluntario, Voluntario de Adopciones, Voluntarios Paseadores, Entrenador Certificado, Personal de Recepción.

**Insumos médicos:**
Vacuna Séxtuple Canina, Vacuna Triple Felina, Vacuna Combinada para Conejos, Vacuna Preventiva para Roedores, Vacuna Combinada para Aves, Ivermectina Oral, Anestesia General (Propofol), Sedantes (Xilazina), Kit Médico Básico, Instrumental Quirúrgico.

**Equipamiento y herramientas:**
Llaves del Refugio, Cámara Digital, Escoba Industrial, Desinfectante, Juguetes Interactivos, Vasijas de Acero, Toallas Absorbentes, Recipiente de Agua, Carpa de Exhibición, Folletos Informativos, Bolsas Sanitarias, Correas y Arneses, Caja de Transporte, Jaula de Transporte, Terrario Especial, Vehículo Petmóvil.

**Alimentos:**
Croquetas Premium (perros), Carne Congelada (serpientes), Heno Premium (conejos), Comida Seca (gatos), Mezcla de cereales y vegetales (roedores), Mezcla de Semillas (aves).

**Animales:**
Perros, Gatos, Conejos, Aves, Serpientes, Roedores.

---

## 🔒 Restricciones del Sistema

Esta es la parte más importante del diseño. Las restricciones modelan las reglas reales del refugio y garantizan que ningún evento pueda planificarse de forma insegura o incoherente.

### Co-requisitos (Restricciones de Inclusión)

Un recurso no puede usarse solo: requiere que otro recurso esté presente en el mismo evento. Esto se implementa en el campo `"associated"` de cada recurso.

**Ejemplos y justificación:**

- **Veterinario → Kit Médico Básico:** Ningún procedimiento médico puede realizarse sin el equipo básico de atención. El veterinario sin su kit no puede trabajar de forma segura.

- **Vacuna Séxtuple Canina → Veterinario + Perros:** Una vacuna canina sin un veterinario que la administre carece de sentido operativo, y sin perros asignados al evento se desperdiciaría un insumo limitado.

- **Cámara Digital → Voluntario de Adopciones:** La cámara se usa exclusivamente para registrar procesos de adopción y generar material de difusión. Sin el voluntario de adopciones, no hay quien la opere dentro de su contexto correcto.

- **Entrenador Certificado → Juguetes Interactivos:** El entrenamiento sin material de estimulación no es efectivo. Los juguetes son parte indispensable de la metodología del entrenador.

- **Carpa de Exhibición → Voluntario + Folletos Informativos:** Una feria de adopción sin voluntarios que atiendan al público y sin material informativo para entregar pierde todo su propósito de difusión.

- **Voluntarios Paseadores → Correas y Arneses + Bolsas Sanitarias:** Por seguridad vial y normativa de espacios públicos, los paseos siempre requieren arnés y gestión de residuos.

- **Correas y Arneses → Perros:** Este equipo de paseo es específico para perros. Reservarlo sin perros asignados no tiene sentido funcional.

- **Personal de Recepción → Llaves del Refugio:** El personal de recepción es el responsable de abrir y cerrar el refugio. Sin las llaves, no puede desempeñar su función principal.

### Exclusiones (Restricciones de Incompatibilidad)

Dos recursos no pueden coexistir en el mismo evento. Esto se implementa en el campo `"exclusions"` de cada recurso.

**Ejemplos y justificación:**

- **Veterinario ❌ Entrenador Certificado:** Un veterinario en medio de un procedimiento médico requiere concentración y un entorno controlado. La presencia simultánea de una sesión de entrenamiento generaría ruido, movimiento y distracción incompatibles con la seguridad del paciente animal.

- **Vacuna Séxtuple Canina ❌ Gatos / Conejos / Aves / Roedores / Serpientes:** Las vacunas están formuladas para especies específicas. Mezclar especies distintas en el mismo evento de vacunación sería un error médico grave y aumenta el riesgo de contagio cruzado entre animales de diferente estado sanitario.

- **Voluntario ❌ Voluntario de Adopciones:** Son perfiles con funciones y responsabilidades distintas. Un voluntario general no está capacitado para guiar procesos de adopción, y combinar ambos roles en el mismo evento generaría confusión sobre las responsabilidades.

- **Carpa de Exhibición ❌ Veterinario:** Una feria de adopción es un evento abierto al público, con ruido y movimiento. Ese ambiente es incompatible con procedimientos veterinarios que requieren condiciones de asepsia y tranquilidad.

- **Anestesia General ❌ Alimentos (Croquetas, Heno, Carne Congelada, etc.):** Por razones de seguridad básica, no se puede tener comida animal cerca de un quirófano activo.

- **Sedantes (Xilazina) ❌ Entrenador Certificado + Juguetes Interactivos:** Los sedantes se usan en contextos de rescate o traslado de animales nerviosos, no en entrenamiento. Combinar ambos sería médicamente contradictorio.

- **Terrario Especial ❌ Conejos / Roedores / Perros / Gatos / Aves:** Por seguridad de los demás animales. Una serpiente fuera de su terrario en presencia de presas naturales genera riesgo inmediato.

---

## ⚙️ Lógica Central: Algoritmo de Detección de Conflictos

El corazón del sistema es la función `resources_available` en `utils.py`. Implementa un algoritmo de **barrido temporal (sweep line)** que verifica si los recursos solicitados están disponibles en el intervalo pedido, y en caso de conflicto, calcula automáticamente el próximo hueco libre.

### Cómo funciona

1. Dado un intervalo `[start, end]` y una lista de recursos seleccionados, el algoritmo ordena todos los eventos existentes por fecha de inicio.

2. Para cada recurso seleccionado, identifica todos los eventos existentes que se solapan con el intervalo pedido.

3. Construye un conjunto de **timestamps relevantes**: los momentos donde algo cambia dentro del intervalo (inicio o fin de algún evento solapante). Estos timestamps dividen el intervalo en sub-intervalos homogéneos.

4. Para cada sub-intervalo, cuenta cuántos eventos usan ese recurso simultáneamente. Si el conteo es mayor o igual a la cantidad disponible (`quantity`), el recurso está bloqueado.

5. Si algún recurso está bloqueado, el algoritmo avanza `current_start` al final del conflicto más cercano y repite el proceso desde esa nueva posición, manteniendo la misma duración.

6. Este proceso se repite hasta encontrar un hueco válido donde todos los recursos estén disponibles.

### Por qué este enfoque es correcto

El algoritmo maneja correctamente todos los casos difíciles: eventos que envuelven completamente el intervalo pedido, eventos parciales (que empiezan antes o terminan después), recursos con quantity > 1 con solapamientos complejos, huecos entre eventos que son demasiado pequeños para la duración pedida, y cadenas de eventos consecutivos.

---

## 🔁 Eventos Recurrentes

La recurrencia permite crear una serie de eventos que se repiten automáticamente con un patrón definido. El sistema:

1. Genera todas las ocurrencias entre la fecha inicial y la fecha límite.
2. Valida cada ocurrencia individualmente contra el calendario existente y contra las demás ocurrencias de la misma serie (para detectar solapamientos internos).
3. Si alguna ocurrencia tiene conflicto, muestra las ocurrencias conflictivas con su sugerencia de horario alternativo y cancela el guardado completo de la serie.
4. Si todas las ocurrencias son válidas, las guarda todas con un `series_id` UUID compartido.

Todas las ocurrencias de una serie pueden eliminarse a la vez gracias a ese identificador compartido.

**Patrones disponibles:**

| Patrón | Delta |
|---|---|
| Diaria | 1 día |
| Semanal | 7 días |
| Mensual | 30 días |

**Restricción:** la recurrencia no puede superar 365 días desde la fecha de inicio, ya que los datos del refugio se restauran anualmente.

---

## 🖼️ Guía de la Interfaz

La interfaz está construida con **Kivy** y **KivyMD**. Todas las pantallas comparten un fondo personalizado, tipografías propias (`Poppins`, `OpenSans`, `Roboto`) y efectos de sonido diferenciados por especie animal al seleccionar recursos.

### 🏠 Pantalla de Inicio

Punto de entrada de la aplicación. Contiene dos botones visuales grandes:
- **Crear evento:** inicia el flujo completo de planificación.
- **Ver eventos creados:** navega al listado de todos los eventos guardados.

### 📍 Pantalla de Lugar

Grid de 8 imágenes representando cada área del refugio. Al seleccionar un lugar, se muestra una pantalla de carga animada antes de cargar los recursos disponibles para ese espacio.

**Lugares disponibles:**
Sala de procedimientos, Sala quirúrgica, Sala de entrevistas, Área de alojamiento, Área de alimentación, Área de baño, Patio de ejercicios, Exterior.

### 🧰 Pantalla de Recursos

Lista scrolleable de todos los recursos disponibles para el lugar seleccionado. Cada recurso muestra su imagen, nombre, descripción y cantidad disponible. Al pulsar un recurso, se resalta en azul y queda seleccionado. Al pulsar de nuevo, se deselecciona.

Al pulsar continuar, el sistema valida en tiempo real todas las restricciones de co-requisitos y exclusiones. Si hay errores, se muestra un popup detallado con todos los problemas encontrados antes de permitir avanzar.

Los sonidos de cada especie (ladrido, maullido, etc.) se reproducen al seleccionar el recurso correspondiente.

### ⏰ Pantalla de Fecha y Hora

Tres campos: título del evento, fecha/hora de inicio y fecha/hora de fin. Los campos de fecha y hora usan el calendario y reloj de **KivyMD** (`MDDatePicker` y `MDTimePicker`) para garantizar un formato correcto y evitar errores de entrada.

El sistema valida:
- Que el título no esté vacío
- Que ambas fechas estén rellenas
- Que la fecha de fin sea posterior a la de inicio
- Que la fecha de inicio no sea anterior al momento actual
- Que la duración no supere 24 horas
- Que ningún recurso seleccionado esté ya ocupado en ese intervalo
- Que la fecha de inicio no esté un año después de la fecha actual

Si hay conflicto de recursos, se muestra el horario alternativo sugerido por el algoritmo.

### 🔁 Pantalla de Recurrencia

Aparece solo si el usuario elige crear un evento recurrente. Permite configurar el patrón (diaria/semanal/mensual) y la fecha límite de la serie. Usa el calendario de KivyMD para seleccionar la fecha límite.

### 📋 Pantalla de Eventos Creados

Lista scrolleable de todos los eventos guardados. Los eventos pasados se muestran en gris para diferenciarlos visualmente de los futuros. Cada tarjeta incluye el título del evento y botones para ver detalles o eliminar.

### 🗑️ Eliminación Inteligente

Al eliminar un evento que pertenece a una serie recurrente, el sistema pregunta si se desea eliminar solo esa ocurrencia o toda la serie. Los eventos sin recurrencia se eliminan directamente.

### 🔎 Detalles del Evento

Popup con información completa: horario de inicio y fin, recursos asignados, patrón de recurrencia e identificador de serie (para series recurrentes).

---

## 💾 Persistencia de Datos

El estado completo de la aplicación se guarda en dos archivos JSON dentro de la carpeta `data/`:

### `data/resources.json`

Define el inventario completo del refugio. Este archivo es el que determina qué recursos existen, cuántos hay de cada uno, en qué lugares pueden usarse y cuáles son sus restricciones. Modificar este archivo permite adaptar la aplicación a un refugio diferente sin cambiar ninguna línea de código.

### `data/events.json`

Almacena todos los eventos planificados. Se actualiza automáticamente cada vez que se crea o elimina un evento. Ejemplo de estructura:

```json
[
  {
    "title": "Vacunación mensual canina",
    "start": "2025-07-01 09:00",
    "end": "2025-07-01 11:00",
    "recurrence": "mensual",
    "until": "2025-12-01",
    "resources": ["Veterinario", "Kit Médico Básico", "Vacuna Séxtuple Canina", "Perros"],
    "place": "sala_de_procedimientos",
    "series_id": "a3f2c1d4-..."
  }
]
```

Si `data/events.json` no existe cuando se ejecuta la aplicación por primera vez, se crea automáticamente vacío. Si el archivo existiera pero estuviera corrupto, la aplicación lo trata como si estuviera vacío para evitar un crash.

---

## 🌳 Árbol de Directorios

```
Planificador-de-Eventos/
├── data/
│   ├── events.json              ← eventos planificados (se genera automáticamente)
│   └── resources.json           ← inventario del refugio
│
├── fonts/
│   └── (tipografías .ttf usadas en la interfaz)
│
├── images/
│   └── (iconos, fondos, botones, imágenes de lugares y recursos)
│
├── sounds/
│   └── bark.mp3, meow.mp3, rabbit.mp3, bird.mp3, snake.mp3, rodent.mp3, click.mp3
│
├── screens/
│   ├── __init__.py              ← convierte la carpeta en paquete Python
│   ├── place.py                 ← PlaceScreen: selección del lugar
│   ├── resources.py             ← ResourcesScreen: selección de recursos
│   ├── date.py                  ← DateScreen: título, fechas y validación
│   ├── events.py                ← EventsScreen: listado, detalles y eliminación
│   └── recurrence.py            ← RecurrenceScreen: configuración de series
│
├── .gitignore
├── requirements.txt
├── main.py                      ← punto de entrada de la aplicación
├── utils.py                     ← lógica de negocio: conflictos, validaciones, I/O
└── widgets.py                   ← widgets reutilizables: RoundedButton, ImageButton, etc.
```

---

## 🚀 Instalación y Ejecución

Sigue estos pasos según tu sistema operativo. Se asume que tienes **Python 3.9 o superior** instalado.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/Planificador-de-Eventos.git
cd Planificador-de-Eventos
```

### 2. Crear y activar un entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
# Si tu política de ejecución no permite scripts:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias principales son `kivy` y `kivymd`. En Linux puede ser necesario instalar dependencias del sistema para Kivy (SDL2, etc.) antes de ejecutar el pip install. Consulta la [documentación oficial de Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html) si encuentras problemas de compilación.

### 4. Ejecutar la aplicación

```bash
python main.py
```

La ventana se abre en tamaño fijo de 800×600 píxeles. El redimensionamiento está desactivado intencionalmente para preservar el layout visual.

---

## 📋 Uso Rápido

**Crear un evento simple:**
1. Pulsa *Crear evento* en la pantalla de inicio.
2. Selecciona el lugar donde se realizará.
3. Selecciona los recursos necesarios. El sistema te avisará si falta algún co-requisito o si hay una exclusión incompatible.
4. Introduce el título y el rango horario usando el calendario y reloj.
5. Si el horario está libre, se te preguntará si el evento es recurrente.
6. Responde *No* para guardar el evento único.

**Crear un evento recurrente:**
1. Sigue los mismos pasos que para un evento simple.
2. Cuando se pregunte por la recurrencia, responde *Sí*.
3. Introduce el patrón (diaria/semanal/mensual) y la fecha límite.
4. El sistema validará cada ocurrencia y, si todas son válidas, las guardará como serie.

**Ver y gestionar eventos:**
1. Pulsa *Eventos creados* en la pantalla de inicio.
2. Los eventos pasados aparecen en gris; los futuros en crema.
3. Usa *Ver detalles* para consultar los recursos, horario y recurrencia de cada evento.
4. Usa *Eliminar* para borrar una ocurrencia o toda la serie.

---

## 📦 Dependencias

| Librería | Uso |
|---|---|
| `kivy` | Framework de interfaz gráfica multiplataforma |
| `kivymd` | Componentes Material Design (calendario, reloj) |
| `json` | Persistencia de datos (incluida en Python) |
| `datetime` | Manejo de fechas e intervalos (incluida en Python) |
| `uuid` | Generación de identificadores de serie (incluida en Python) |

---

*Hecho con amor 🐾 para todos los animales que esperan una familia.*
