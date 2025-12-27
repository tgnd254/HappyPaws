import json
from datetime import datetime

class Resources:
    def __init__(self,name,type,description,associated,exclusions):
        self.name=name
        self.type=type
        self.description=description
        self.associated=associated
        self.exclusions=exclusions

def load_resources():
    file=open("recursos.json","r",encoding="utf-8")
    data=json.load(file)
    file.close()
    return data

resources=load_resources()

class Event:
    def __init__(self,name,resources,start,end):
        self.name=name
        self.resources=resources
        self.start=start
        self.end=end

def load_events():
    try:
        file=open("eventos.json","r",encoding="utf-8")
        data=json.load(file)
        file.close()
        return data
    except FileNotFoundError:
        return []
    
def save_events(events):
    file=open("eventos.json","w",encoding="utf-8")
    json.dump(events,file,indent=1,ensure_ascii=False)
    file.close()

def check_date(date):
    while True:
        text=input(date)
        try:
            return datetime.strptime(text,"%Y-%m-%d %H:%M")
        except ValueError:
            print("La fecha introducida no es valida")

def check_validity(new_event, events, resources):

    nstart=datetime.strptime(new_event["start"], "%Y-%m-%d %H:%M")
    nend=datetime.strptime(new_event["end"], "%Y-%m-%d %H:%M")
    nresources=new_event["resources"]

    for nr in nresources:
        r=next((x for x in resources if x["name"]==nr), None)
        if r:
            for exc in r.get("exclusions"):
                if exc in nresources:
                    return False, f"{r["name"]} no puede ser usado junto a {exc}"   
            for asc in r.get("associated"):
                if asc not in nresources:
                    return False, f"{r["name"]} requiere {asc}"
    
    for e in events:
        estart=datetime.strptime(e["start"], "%Y-%m-%d %H:%M")
        eend=datetime.strptime(e["end"], "%Y-%m-%d %H:%M")
        if not(nend<=estart or nstart>=eend):
            used=set(e["resources"])
            necessary=set(nresources)
            if used.intersection(necessary):
                return False, "Algunos de los recursos requeridos estan siendo utilizados"
            
    return True, "Evento creado"
        
name = input("Introduce el nombre del evento: ")
start = check_date("Introduce la fecha y hora de inicio (YYYY-MM-DD HH:MM): ")
end = check_date("Introduce la fecha y hora de fin (YYYY-MM-DD HH:MM): ")
if start>=end:
    print("La fecha de inicio debe ser menor que la de fin")
else:
    resources_input=input("Introduce los recursos separados por comas: ")
    resources=[r.strip() for r in resources_input.split(",")]

new_event=Event(name,resources,start,end)
events=load_events()

valid,message=check_validity(new_event.to_dict(),events,resources)
print(message)

if valid:
    events.append(new_event.to_dict())
    save_events(events)


