
import json
from datetime import datetime

# Cargar eventos
def load_events():
    try:
        with open("data/events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar eventos
def save_events(events):
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

# Cargar recursos
def load_resources():
    with open("data/resources.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Metodo para verificar disponibilidad de recursos 
def resources_available(start,end,selected,resources,events):
    duration=end-start
    current_start,current_end=start,end
    occupated_resources_set=set() # Mantener registro de recursos ocupados
    events_sorted = sorted(events, key=lambda ev: ev["start"]) # Ordenar eventos por fecha de inicio

    while True:
        unavailable=[]
        for sr in selected:
            count=0 # Contador de eventos que utilizan el recurso

            # Obtener la cantidad del recurso
            for r in resources:
                if r["name"]==sr:
                    quantity=r["quantity"]
                    break

            for ev in events_sorted:
                ev_start = datetime.strptime(ev["start"], "%Y-%m-%d %H:%M") 
                ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M") 
                if not (current_end <= ev_start or current_start >= ev_end): # Verificar solapamiento
                    if sr in ev["resources"]:
                        count+=1

            # Verificar si el recurso está disponible
            if count>=quantity:
                unavailable.append(sr)

        occupated_resources_set.update(unavailable)

        # Si no hay recursos no disponibles devolver la fecha actual
        if not unavailable: 
            return current_start, current_end, list(occupated_resources_set)
        
        conflicts_ends=[]
        for ev in events_sorted:
            ev_start = datetime.strptime(ev["start"], "%Y-%m-%d %H:%M") 
            ev_end = datetime.strptime(ev["end"], "%Y-%m-%d %H:%M")
            for r in unavailable:
                if r in ev["resources"]:
                    if not (current_end <= ev_start or current_start >= ev_end): # Verificar solapamiento
                        conflicts_ends.append(ev_end)
                    break

        # Si hay conflictos, avanzar al final del conflicto más cercano
        if conflicts_ends:
            current_start=max(conflicts_ends)
            current_end=current_start+duration
        else: # No hay forma de avanzar 
            return None, None, list(occupated_resources_set)

# Metodo para verificar que no hayan conflictos entre los recursos
def validate_resources(resources, selected_resources):
    errors = []
    for r in resources:
        name = r["name"]
        if name in selected_resources:
            for excl in r.get("exclusions", []):
                if excl in selected_resources:
                    errors.append(f" {name} no puede usarse junto a {excl}")
            for assoc in r.get("associated", []):
                if assoc not in selected_resources:
                    errors.append(f" {name} requiere {assoc}")
    return errors

