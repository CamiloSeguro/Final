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
    /* ---- Ancho y espaciado ---- */
    .block-container{
      padding-top: .5rem !important;
      padding-bottom: 1rem !important;
      max-width: 1400px !important;      /* ancho cómodo */
      margin: 0 auto !important;
      overflow: visible !important;       /* <— evita clip */
    }
    /* evita clip en filas/columnas internas */
    [data-testid="stHorizontalBlock"],
    [data-testid="stVerticalBlock"],
    .stColumn { overflow: visible !important; }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
      width: 250px !important;
      background: #0f1624;
      border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* ---- Hero / Cards ---- */
    .hero{
      width: 100%;                        /* <— ocupa todo el ancho del contenedor */
      margin: 0 auto;
      padding:22px 28px; border-radius:18px;
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      border:1px solid rgba(255,255,255,.08);
      box-shadow: 0 0 35px rgba(34,197,94,.18);  /* sombra visible */
    }
    .card{
      padding:18px; border-radius:16px;
      background:#0e1420; border:1px solid rgba(255,255,255,.08);
      box-shadow: 0 0 15px rgba(0,0,0,.25);
    }
    .pill{ display:inline-flex; gap:8px; align-items:center; padding:6px 10px; border-radius:999px;
      border:1px solid rgba(255,255,255,.08); background:rgba(34,197,94,.12); font-size:13px; }
    .pill.bad{ background:rgba(239,68,68,.15); }
    .primary-btn button{ width:100%; padding:10px 14px; font-weight:700; border-radius:10px;
      background:#22c55e !important; color:white !important; border:none !important; }
    </style>
    """, unsafe_allow_html=True)


def connection_pill(connected: bool, last_ts: float|None):
    if connected:
        age = 0 if last_ts is None else int(time.time() - last_ts)
        return f'<span class="pill">🟢 Conectado · {age}s</span>'
    return '<span class="pill bad">🔴 Desconectado</span>'
