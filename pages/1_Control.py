import time
import streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES, inject_css, connection_pill

TOPIC_CMD = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

# --- Estilo global ---
inject_css(st)
st.set_page_config(page_title="SmartLight - Control", page_icon="💡", layout="wide")

# --- Estado inicial ---
if "state" not in st.session_state:
    st.session_state.state = {"sala": False, "cocina": False, "habitacion": False}
if "_connected" not in st.session_state:
    st.session_state._connected = False
if "_last" not in st.session_state:
    st.session_state._last = None

# --- Conexión MQTT ---
bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge
    st.session_state._connected = True

    def on_state(topic, payload):
        st.session_state.state.update({
            k: bool(v) for k, v in payload.items()
            if k in st.session_state.state
        })
        st.session_state._last = time.time()

    bridge.subscribe(TOPIC_STATE, on_state)

# --- Header ---
st.title("💡 Control de Luces")
st.markdown(connection_pill(
    st.session_state._connected,
    st.session_state._last
), unsafe_allow_html=True)

# --- Controles principales ---
st.write("### Habitaciones")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.subheader("🟡 Sala")
        st.caption("Encender o apagar la luz principal")
        sala = st.toggle("Encendida", value=st.session_state.state["sala"], key="sala")

with col2:
    with st.container(border=True):
        st.subheader("⚪ Cocina")
        st.caption("Control de la luz de cocina")
        cocina = st.toggle("Encendida", value=st.session_state.state["cocina"], key="cocina")

with col3:
    with st.container(border=True):
        st.subheader("🔵 Habitación")
        st.caption("Control de la luz de habitación")
        habitacion = st.toggle("Encendida", value=st.session_state.state["habitacion"], key="habitacion")

# --- Botón principal ---
st.divider()
st.button(
    "🚀 Enviar estado",
    type="primary",
    use_container_width=True,
    on_click=lambda: st.session_state._bridge.publish(
        TOPIC_CMD,
        {"sala": sala, "cocina": cocina, "habitacion": habitacion},
    ),
)

# --- Escenas rápidas ---
st.write("### 🎛️ Escenas rápidas")

cols = st.columns(4)
def send_scene(payload, label):
    st.session_state._bridge.publish(TOPIC_CMD, payload)
    st.toast(f"Escena enviada: {label}")

if cols[0].button("🌙 Noche", use_container_width=True):
    send_scene(SCENES["noche"], "Noche")

if cols[1].button("🧠 Trabajo", use_container_width=True):
    send_scene(SCENES["trabajo"], "Trabajo")

if cols[2].button("🔆 Todo ON", use_container_width=True):
    send_scene(SCENES["todo_on"], "Todo ON")

if cols[3].button("🌑 Todo OFF", use_container_width=True):
    send_scene(SCENES["todo_off"], "Todo OFF")

st.caption("Estado actual (MQTT): " + str(st.session_state.state))
