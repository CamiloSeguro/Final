import time, math, streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES

TOPIC_CMD   = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

# ---------- CSS del dashboard ----------
st.markdown("""
<style>
/* Layout general */
.card {background:#fff; border:1px solid #E5E7EB; border-radius:18px; padding:16px;}
.kpi {display:flex; gap:8px; align-items:center; font-weight:600;}
.badge {padding:6px 10px; border-radius:999px; background:#EEF2FF; color:#3730A3; font-weight:700; font-size:12px;}
.section-title {font-weight:800; font-size:18px; margin:0}

/* Botón rojo */
.btn-primary {background:#EF4444; color:#fff; border:none; padding:10px 14px; font-weight:800; border-radius:12px;}
.btn-primary:hover {filter:brightness(.95)}

/* Switch row de Lights */
.light-row {display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px dashed #E5E7EB;}
.light-row:last-child {border-bottom:none}

/* Tarjetas de dispositivos */
.device {text-align:center; background:#EEF2FF; border:1px dashed #CBD5E1; padding:18px; border-radius:16px;}
.device h5 {margin:10px 0 0 0}

/* Tabs inferiores */
.room-tabs .stTabs [role="tab"] {font-weight:800}

/* Dial circular (HTML) */
.dial-wrap {display:grid; place-items:center; padding:8px}
.dial {
  --val: 25; /* grados simulados para UI */
  width: 240px; height: 240px; border-radius:50%;
  background:
    conic-gradient(#7C83FF calc(var(--val)*3.6deg), #E5E7EB 0),
    radial-gradient(#fff 62%, transparent 63%);
  box-shadow: inset 0 4px 12px rgba(0,0,0,.08);
  display:grid; place-items:center;
}
.dial .val {font-size:34px; font-weight:900; color:#111827}
.dial .sub {font-size:12px; color:#6B7280}
</style>
""", unsafe_allow_html=True)

# ---------- estado ----------
if "state" not in st.session_state:
    st.session_state.state = {"sala": False, "cocina": False, "habitacion": False}
if "_connected" not in st.session_state: st.session_state._connected = False
if "_last" not in st.session_state: st.session_state._last = None

# ---------- MQTT ----------
bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge
    st.session_state._connected = True

    def on_state(topic, payload):
        st.session_state.state.update({k: bool(v) for k, v in payload.items() if k in st.session_state.state})
        st.session_state._last = time.time()

    bridge.subscribe(TOPIC_STATE, on_state)

# ---------- Header ----------
c_logo, c_title, c_btn = st.columns([1,3,1])
with c_logo:
    st.markdown("### DashIoT")
with c_title:
    st.markdown("## Good Morning!, Camilo.")
    st.caption("Have a nice day ✨")
with c_btn:
    st.markdown("<div style='text-align:right'>", unsafe_allow_html=True)
    st.button("➕ New Device", key="newdev", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # espacio

# ---------- Fila principal (dial + cámara + lights) ----------
left, right = st.columns([2,1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Air Conditioner</div>', unsafe_allow_html=True)
    st.caption("Swing • Manual")
    # Dial (decorativo para UI del mock)
    st.markdown('<div class="dial-wrap"><div class="dial"><div class="val">25°C</div><div class="sub">47% Humidity</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    # Camera preview (placeholder)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1600607687920-4ce9ce8b3c87?q=80&w=1200&auto=format&fit=crop", caption="Live • Living Room", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    # Lights card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Lights</div>', unsafe_allow_html=True)
    sala = st.toggle("Living Room", value=st.session_state.state["sala"], key="sala")
    cocina = st.toggle("Kitchen", value=st.session_state.state["cocina"], key="cocina")
    habitacion = st.toggle("Bed Room", value=st.session_state.state["habitacion"], key="habitacion")
    st.button("Apply", key="apply_lights",
              on_click=lambda: st.session_state._bridge.publish(TOPIC_CMD, {
                  "sala": sala, "cocina": cocina, "habitacion": habitacion
              }))
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ---------- Dispositivos (AC/TV/Speaker) ----------
d1, d2, d3 = st.columns(3)
with d1:
    st.markdown('<div class="device">❄️<h5>AC</h5><div class="badge">On</div></div>', unsafe_allow_html=True)
with d2:
    st.markdown('<div class="device">📺<h5>TV</h5><div class="badge" style="background:#FEE2E2;color:#991B1B">Off</div></div>', unsafe_allow_html=True)
with d3:
    st.markdown('<div class="device">🔊<h5>Speaker</h5><div class="badge">On</div></div>', unsafe_allow_html=True)

st.write("")

# ---------- Tabs de habitaciones ----------
st.markdown('<div class="room-tabs">', unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Living Room", "Bed Room", "Kitchen", "Bathroom", "Garage"])
with tab1:
    st.markdown('<div class="card">Living Room • Tips: Ajusta escenas rápidas abajo.</div>', unsafe_allow_html=True)
with tab2:
    st.markdown('<div class="card">Bed Room • Buenas noches 😴</div>', unsafe_allow_html=True)
with tab3:
    st.markdown('<div class="card">Kitchen • Recetas y temporizadores pronto.</div>', unsafe_allow_html=True)
with tab4:
    st.markdown('<div class="card">Bathroom • Sensor humedad próximamente.</div>', unsafe_allow_html=True)
with tab5:
    st.markdown('<div class="card">Garage • Puerta inteligente próximamente.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ---------- Escenas (como en la maqueta, parte inferior) ----------
e1, e2, e3, e4 = st.columns(4)
def send_scene(payload, label):
    st.session_state._bridge.publish(TOPIC_CMD, payload)
    st.toast(label)

with e1:
    if st.button("🌙 Noche", use_container_width=True):
        send_scene(SCENES["noche"], "Scene: Night")
with e2:
    if st.button("🧠 Trabajo", use_container_width=True):
        send_scene(SCENES["trabajo"], "Scene: Work")
with e3:
    if st.button("🔆 Todo ON", use_container_width=True):
        send_scene(SCENES["todo_on"], "All ON")
with e4:
    if st.button("🌑 Todo OFF", use_container_width=True):
        send_scene(SCENES["todo_off"], "All OFF")

st.caption("Estado actual (MQTT): " + str(st.session_state.state))
