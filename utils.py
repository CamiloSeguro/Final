import os, time

SCENES = {
    "noche":      {"sala": False, "cocina": False, "habitacion": True},
    "trabajo":    {"sala": True,  "cocina": True,  "habitacion": False},
    "todo_on":    {"sala": True,  "cocina": True,  "habitacion": True},
    "todo_off":   {"sala": False, "cocina": False, "habitacion": False},
}

def parse_command(text: str):
    t = (text or "").lower()
    payload = {}
    for room in ["sala", "cocina", "habitación", "habitacion"]:
        if (("encender" in t) or ("prender" in t)) and room in t:
            payload[_norm(room)] = True
        if "apagar" in t and room in t:
            payload[_norm(room)] = False
    if "escena" in t or "modo" in t:
        if "noche" in t: payload.update(SCENES["noche"])
        if "trabajo" in t: payload.update(SCENES["trabajo"])
        if "todo" in t and (("on" in t) or ("encender" in t)): payload.update(SCENES["todo_on"])
        if "todo" in t and (("off" in t) or ("apagar" in t)):  payload.update(SCENES["todo_off"])
    if "apagar todo" in t or "todo off" in t: payload.update(SCENES["todo_off"])
    if "encender todo" in t or "todo on" in t: payload.update(SCENES["todo_on"])
    return payload

def _norm(room: str): return "habitacion" if room.startswith("habita") else room
def current_broker(): return os.getenv("MQTT_BROKER", "broker.hivemq.com")

def inject_css(st):
    st.markdown("""
    <style>
    /* Área principal: más ancha y sin recortes */
    .block-container{
      max-width: 1300px !important;
      margin: 0 auto !important;
      padding-top: .5rem !important;
      padding-bottom: 1rem !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    .stColumn { overflow: visible !important; }

    /* Hero “card” centrada: usamos ancho fijo y SIN box-shadow para no cortar */
    .hero{
      width: 860px;                /* <- ancho fijo centrado */
      margin: 0 auto;              /* <- centra */
      padding: 22px 28px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      border: 1px solid rgba(255,255,255,.10);
    }

    /* Cards habituales (sin sombras pesadas) */
    .card{
      padding:18px; border-radius:16px;
      background:#0e1420; border:1px solid rgba(255,255,255,.10);
    }

    .pill{ display:inline-flex; gap:8px; align-items:center; padding:6px 10px; border-radius:999px;
      border:1px solid rgba(255,255,255,.10); background:rgba(34,197,94,.14); font-size:13px; }
    .pill.bad{ background:rgba(239,68,68,.18); }
    .primary-btn button{ width:100%; padding:10px 14px; font-weight:700; border-radius:10px;
      background:#22c55e !important; color:white !important; border:none !important; }
    </style>
    """, unsafe_allow_html=True)



def connection_pill(connected: bool, last_ts: float|None):
    if connected:
        age = 0 if last_ts is None else int(time.time() - last_ts)
        return f'<span class="pill">🟢 Conectado · {age}s</span>'
    return '<span class="pill bad">🔴 Desconectado</span>'
