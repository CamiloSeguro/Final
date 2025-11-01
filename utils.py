SCENES = {
    "noche":      {"sala": False, "cocina": False, "habitacion": True},
    "trabajo":    {"sala": True,  "cocina": True,  "habitacion": False},
    "todo_on":    {"sala": True,  "cocina": True,  "habitacion": True},
    "todo_off":   {"sala": False, "cocina": False, "habitacion": False},
}

def parse_command(text: str):
    t = (text or "").lower()
    payload = {}
    # Habitación específica
    for room in ["sala", "cocina", "habitación", "habitacion"]:
        if (("encender" in t) or ("prender" in t)) and room in t:
            payload[_norm(room)] = True
        if "apagar" in t and room in t:
            payload[_norm(room)] = False
    # Escenas
    if "escena" in t or "modo" in t:
        if "noche" in t: payload.update(SCENES["noche"])
        if "trabajo" in t: payload.update(SCENES["trabajo"])
        if "todo" in t and (("on" in t) or ("encender" in t)): payload.update(SCENES["todo_on"])
        if "todo" in t and (("off" in t) or ("apagar" in t)):  payload.update(SCENES["todo_off"])
    # Comandos globales simples
    if "apagar todo" in t or "todo off" in t:
        payload.update(SCENES["todo_off"])
    if "encender todo" in t or "todo on" in t:
        payload.update(SCENES["todo_on"])
    return payload

def _norm(room: str):
    return "habitacion" if room.startswith("habita") else room
