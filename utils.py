import time
import os

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
    # Comandos globales
    if "apagar todo" in t or "todo off" in t:
        payload.update(SCENES["todo_off"])
    if "encender todo" in t or "todo on" in t:
        payload.update(SCENES["todo_on"])
    return payload

def _norm(room: str):
    return "habitacion" if room.startswith("habita") else room

# ---------- UI helpers ----------
def inject_css(st):
    st.markdown("""
    <style>
    .hero {
      padding: 18px 22px; border-radius: 16px;
      background: linear-gradient(135deg, #0b0f15 0%, #111827 100%);
      border: 1px solid rgba(255,255,255,.06);
    }
    .card {
      padding: 16px; border-radius: 14px;
      background: #0e1420; border: 1px solid rgba(255,255,255,.06);
    }
    .pill {
      display:inline-flex; align-items:center; gap:8px;
      padding:6px 10px; border-radius:999px; font-size:13px;
      border: 1px solid rgba(255,255,255,.08);
      background: rgba(34,197,94,.12);
    }
    .pill.bad { background: rgba(239,68,68,.12); }
    .pill.neutral { background: rgba(148,163,184,.12); }
    .chips { display:flex; flex-wrap:wrap; gap:8px; }
    .chip {
      padding:6px 10px; border-radius:999px; font-size:12px;
      background:#0f172a; border:1px solid rgba(255,255,255,.08);
      cursor:pointer; user-select:none;
    }
    </style>
    """, unsafe_allow_html=True)

def connection_pill(connected: bool, last_ts: float|None):
    if connected:
        age = 0 if last_ts is None else int(time.time() - last_ts)
        return f'<span class="pill">🟢 Conectado <small>{age}s</small></span>'
    else:
        return '<span class="pill bad">🔴 Desconectado</span>'

def current_broker():
    return os.getenv("MQTT_BROKER", "broker.hivemq.com")
