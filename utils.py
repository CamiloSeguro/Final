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

# ---------- Brand helpers ----------
def current_broker(): return os.getenv("MQTT_BROKER", "broker.hivemq.com")

def inject_style(blueprint: bool=False):
    # colores base y blueprint
    if blueprint:
        bg0 = "#030711"
        bg1 = "#071426"
        grid = "rgba(80,160,255,.12)"
        accent = "#60A5FA"   # azul
        glow = "rgba(96,165,250,.45)"
    else:
        bg0 = "#05070B"
        bg1 = "#0A0F18"
        grid = "rgba(34,197,94,.12)"
        accent = "#22C55E"   # verde
        glow = "rgba(34,197,94,.45)"

    css = f"""
    <style>
    /* ===== Background animado + grid ===== */
    .appview-container {{
      background:
        radial-gradient(1000px 600px at 20% -10%, {glow} 0%, transparent 60%),
        radial-gradient(800px 500px at 120% 20%, {glow} 0%, transparent 65%),
        linear-gradient(180deg, {bg0} 0%, {bg1} 100%);
    }}
    body::before {{
      content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
      background-image:
        repeating-linear-gradient(0deg, {grid}, {grid} 1px, transparent 1px, transparent 32px),
        repeating-linear-gradient(90deg, {grid}, {grid} 1px, transparent 1px, transparent 32px);
      mask: linear-gradient(to bottom, rgba(0,0,0,.8), rgba(0,0,0,.2));
    }}
    /* ===== Navbar ===== */
    .navbar {{
      display:flex; gap:12px; align-items:center; margin: 6px 0 18px 0;
    }}
    .navbtn {{
      padding:8px 12px; border-radius:12px; border:1px solid rgba(255,255,255,.08);
      background:rgba(255,255,255,.03); color:#E6F6EC; text-decoration:none;
      transition:.2s; font-weight:600; box-shadow:0 0 0 0 transparent;
    }}
    .navbtn:hover {{ transform: translateY(-1px); box-shadow:0 6px 24px {glow}; border-color:{accent}33; }}
    /* ===== Cards glass ===== */
    .card {{
      position:relative; padding:16px; border-radius:18px; overflow:hidden;
      background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      border: 1px solid rgba(255,255,255,.08);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.04), 0 10px 40px rgba(0,0,0,.35);
    }}
    .card h4 {{ margin:0 0 8px 0; }}
    /* ===== Pills ===== */
    .pill {{ display:inline-flex; gap:8px; align-items:center; padding:6px 10px; border-radius:999px;
            border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.05); font-size:13px; }}
    .ok {{ background: {accent}22; }}
    .bad {{ background: #ef444422; }}
    /* ===== Scene buttons ===== */
    .scene {{
      width:100%; padding:14px 16px; border-radius:16px; border:1px solid rgba(255,255,255,.08);
      background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      font-weight:700; cursor:pointer; transition: .15s transform, .3s box-shadow;
    }}
    .scene:hover {{ transform: translateY(-2px); box-shadow:0 14px 40px {glow}; }}
    /* ===== Glow cuando ON ===== */
    .light-on {{ box-shadow: 0 0 0 0 {glow}, 0 0 32px {glow} inset; }}
    /* ===== Bulb preview ===== */
    .bulb {{
      width:110px; aspect-ratio:1/1; border-radius:999px; margin:auto;
      background: radial-gradient(circle at 50% 60%, #FFD166 0%, #FDBA74 35%, transparent 65%);
      filter: drop-shadow(0 0 30px {glow});
      opacity:.1; transition:.25s;
    }}
    .bulb.on {{ opacity: .9; }}
    </style>
    """
    return css

def connection_pill(connected: bool, last_ts: float|None):
    if connected:
        age = 0 if last_ts is None else int(time.time() - last_ts)
        return f'<span class="pill ok">🟢 Conectado · {age}s</span>'
    return '<span class="pill bad">🔴 Desconectado</span>'
