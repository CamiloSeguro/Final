import time, streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES, inject_css, connection_pill

TOPIC_CMD = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

inject_css(st)

if "state" not in st.session_state:
    st.session_state.state = {"sala": False, "cocina": False, "habitacion": False}
if "_connected" not in st.session_state: st.session_state._connected = False
if "_last" not in st.session_state: st.session_state._last = None

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

st.markdown("## 💡 Control")
st.markdown(connection_pill(st.session_state._connected, st.session_state._last), unsafe_allow_html=True)

# Tiles simples
col1, col2, col3 = st.columns(3)
def tile(col, key, title, emoji):
    with col:
        def card(html: str):
    st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)

card("""
  <h4>🟡 Sala</h4>
  <p style="opacity:.75;margin:0">Encender/Apagar</p>
""")
        val = st.toggle(f"{emoji} {title}", value=st.session_state.state[key], key=key)
        st.caption("Encender/Apagar")
        st.markdown('</div>', unsafe_allow_html=True)
        return val

sala = tile(col1, "sala", "Sala", "🟡")
cocina = tile(col2, "cocina", "Cocina", "⚪")
hab = tile(col3, "habitacion", "Habitación", "🔵")

st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
st.button("🚀 Enviar estado", type="primary",
          on_click=lambda: st.session_state._bridge.publish(
              TOPIC_CMD, {"sala": sala, "cocina": cocina, "habitacion": hab}
          ))
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.subheader("🎛️ Escenas")
cA, cB, cC, cD = st.columns(4)
def send_scene(payload, label):
    st.session_state._bridge.publish(TOPIC_CMD, payload); st.toast(label)
if cA.button("🌙 Noche", use_container_width=True): send_scene(SCENES["noche"], "Noche")
if cB.button("🧠 Trabajo", use_container_width=True): send_scene(SCENES["trabajo"], "Trabajo")
if cC.button("🔆 Todo ON", use_container_width=True): send_scene(SCENES["todo_on"], "Todo ON")
if cD.button("🌑 Todo OFF", use_container_width=True): send_scene(SCENES["todo_off"], "Todo OFF")

st.caption("Estado actual: " + str(st.session_state.state))
