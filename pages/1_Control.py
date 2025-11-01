import time, streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES, inject_css, connection_pill

TOPIC_CMD = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

inject_css(st)

if "state" not in st.session_state:
    st.session_state.state = {"sala": False, "cocina": False, "habitacion": False}
if "_connected" not in st.session_state:
    st.session_state._connected = False
if "_last" not in st.session_state:
    st.session_state._last = None

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

# Header
st.markdown("## 💡 Control")
st.markdown(
    connection_pill(
        connected=st.session_state._connected,
        last_ts=st.session_state._last
    ),
    unsafe_allow_html=True
)

# Cards por habitación
col1, col2, col3 = st.columns(3)

def room_card(col, name_key, title, emoji):
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### {emoji} {title}")
        val = st.toggle("Encendida", value=st.session_state.state[name_key], key=name_key)
        st.caption("Consejo: puedes encender/apagar varias y luego enviar.")
        st.markdown('</div>', unsafe_allow_html=True)
        return val

sala = room_card(col1, "sala", "Sala", "🟡")
cocina = room_card(col2, "cocina", "Cocina", "⚪")
hab = room_card(col3, "habitacion", "Habitación", "🔵")

st.button("🚀 Enviar estado", type="primary",
          on_click=lambda: st.session_state._bridge.publish(
              TOPIC_CMD, {"sala": sala, "cocina": cocina, "habitacion": hab}
          ))

st.divider()
st.subheader("🎛️ Escenas rápidas")

cA, cB, cC, cD = st.columns(4)
def send_scene(payload, label):
    st.session_state._bridge.publish(TOPIC_CMD, payload)
    st.toast(label)

with cA:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🌙 Noche", use_container_width=True): send_scene(SCENES["noche"], "Escena Noche")
    st.markdown('</div>', unsafe_allow_html=True)
with cB:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🧠 Trabajo", use_container_width=True): send_scene(SCENES["trabajo"], "Escena Trabajo")
    st.markdown('</div>', unsafe_allow_html=True)
with cC:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🔆 Todo ON", use_container_width=True): send_scene(SCENES["todo_on"], "Todo ON")
    st.markdown('</div>', unsafe_allow_html=True)
with cD:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🌑 Todo OFF", use_container_width=True): send_scene(SCENES["todo_off"], "Todo OFF")
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Estado actual: " + str(st.session_state.state))
