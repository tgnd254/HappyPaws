
import json
from datetime import datetime,timedelta

# Cargar eventos
def load_events():
    try:
        with open("data/events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Guardar eventos
def save_events(events):
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

# Cargar recursos
def load_resources():
    with open("data/resources.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Metodo para verificar disponibilidad de recursos y buscar el siguiente hueco libre si existen colisiones
def resources_available(start,end,selected,resources,events):
    duration=end-start
    current_start,current_end=start,end
    occupated_resources_set=set() # Mantener registro de recursos ocupados

    resource_quantities = {r["name"]: r["quantity"] for r in resources} #Mapear recursos a sus cantidades

    events_sorted = []
    for ev in events:
        events_sorted.append({
            "start": datetime.strptime(ev["start"], "%Y-%m-%d %H:%M"),
            "end": datetime.strptime(ev["end"], "%Y-%m-%d %H:%M"),
            "resources": ev["resources"]
        })
    events_sorted.sort(key=lambda ev: ev["start"]) #Eventos ordenados por su fecha de inicio

    while True:
        unavailable=[]
        for sr in selected:
            max_quantity=resource_quantities.get(sr,0) #Obtener la cantidad del recurso
            overlapping_events=[]

            for ev in events_sorted:
                if current_end > ev["start"] and current_start < ev["end"]: # Verificar solapamiento
                    if sr in ev["resources"]:
                        overlapping_events.append(ev)

            #Si no hay solapamientos se pasa al siguiente recurso
            if not overlapping_events:
                continue
            
            #Guardar los puntos de cambio dentro del intervalo del evento deseado(cuando termina o empieza un nuevo evento)
            timestamps={current_start,current_end}
            for ev in overlapping_events:
                if current_start<ev["start"]<current_end:
                    timestamps.add(ev["start"])
                if current_start<ev["end"]<current_end:
                    timestamps.add(ev["end"])

            sorted_timestamps = sorted(list(timestamps))
            
            #Por cada subintervalo verifico la cantidad del recurso que esta siendo usado
            resource_blocked=False
            for i in range(len(sorted_timestamps)-1):
                sub_start=sorted_timestamps[i]
                sub_end=sorted_timestamps[i+1]

                count=0
                for ev in overlapping_events:
                    if ev["start"] <= sub_start and ev["end"] >= sub_end:
                        count+=1
                
                #Si la cantidad siendo usada es mayor o igual a la cantidad existente en el refugio entonces hay un conflicto
                if count>=max_quantity:
                    resource_blocked=True
                    break
                
            if resource_blocked:
                unavailable.append(sr)

        occupated_resources_set.update(unavailable)

        # Si no hay recursos ocupados en este intervalo, devolver la fecha actual
        if not unavailable: 
            return current_start, current_end, list(occupated_resources_set)
        
        conflicts_ends=[]
        for ev in events_sorted:
            for r in unavailable:
                if r in ev["resources"]:
                    if current_end > ev["start"] and current_start < ev["end"]: # Verificar solapamiento
                        conflicts_ends.append(ev["end"])
                    break

        # Si hay conflictos, avanzar al final del conflicto más cercano
        if conflicts_ends:
            next_start=min(conflicts_ends)
            #Evitar bucles infinitos por si acaso
            if next_start<=current_start:
                current_start = current_start + timedelta(minutes=1)
            else: 
                current_start=next_start

            current_end=current_start+duration
        else: # No hay forma de avanzar(no hay eventos futuros que liberen recursos)
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

