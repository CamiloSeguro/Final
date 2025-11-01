import time, streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES, inject_style, connection_pill

TOPIC_CMD = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

bp = st.sidebar.session_state.get("🔷 Blueprint mode", False)  # lectura del toggle del sidebar global
st.markdown(inject_style(blueprint=bp), unsafe_allow_html=True)

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

st.markdown("### 💡 Control")
st.markdown(connection_pill(st.session_state._connected, st.session_state._last), unsafe_allow_html=True)

# Bulb preview segun cuantas ON
on_count = sum(1 for v in st.session_state.state.values() if v)
st.write("")
st.markdown(f'<div class="bulb {"on" if on_count>0 else ""}"></div>', unsafe_allow_html=True)
st.caption(f"Luces encendidas: **{on_count}/3**")

# Tiles
col1, col2, col3 = st.columns(3)
def tile(col, key, title, emoji):
    with col:
        on = st.toggle(f"{emoji} {title}", value=st.session_state.state[key], key=key)
        # caja con glow visual
        box = f'<div class="card {"light-on" if on else ""}"><b>Estado:</b> {"ON" if on else "OFF"}</div>'
        st.markdown(box, unsafe_allow_html=True)
        return on

sala = tile(col1, "sala", "Sala", "🟡")
cocina = tile(col2, "cocina", "Cocina", "⚪")
hab = tile(col3, "habitacion", "Habitación", "🔵")

st.button("🚀 Enviar estado", type="primary",
          on_click=lambda: st.session_state._bridge.publish(TOPIC_CMD,
                    {"sala": sala, "cocina": cocina, "habitacion": hab}))

st.divider()
st.markdown("#### 🎛️ Escenas rápidas")

cA, cB, cC, cD = st.columns(4)
def send_scene(payload, label):
    st.session_state._bridge.publish(TOPIC_CMD, payload)
    st.toast(label)

with cA:
    if st.button("🌙 Noche", use_container_width=True, key="scene_noche"):
        send_scene(SCENES["noche"], "Escena Noche")
with cB:
    if st.button("🧠 Trabajo", use_container_width=True, key="scene_work"):
        send_scene(SCENES["trabajo"], "Escena Trabajo")
with cC:
    if st.button("🔆 Todo ON", use_container_width=True, key="scene_on"):
        send_scene(SCENES["todo_on"], "Todo ON")
with cD:
    if st.button("🌑 Todo OFF", use_container_width=True, key="scene_off"):
        send_scene(SCENES["todo_off"], "Todo OFF")

st.caption("Estado actual: " + str(st.session_state.state))
