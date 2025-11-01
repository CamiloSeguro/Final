import time, streamlit as st
from mqtt_client import MqttBridge
from utils import SCENES

TOPIC_CMD = "eafit/camilo/smartlight/commands"
TOPIC_STATE = "eafit/camilo/smartlight/state"

if "state" not in st.session_state:
    st.session_state.state = {"sala": False, "cocina": False, "habitacion": False}

bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge
    def on_state(topic, payload):
        st.session_state.state.update({k: bool(v) for k, v in payload.items() if k in st.session_state.state})
        st.session_state._last = time.time()
    bridge.subscribe(TOPIC_STATE, on_state)

st.title("💡 Control")
col1, col2, col3 = st.columns(3)
with col1:
    sala = st.toggle("Sala", value=st.session_state.state["sala"], key="sala")
with col2:
    cocina = st.toggle("Cocina", value=st.session_state.state["cocina"], key="cocina")
with col3:
    hab = st.toggle("Habitación", value=st.session_state.state["habitacion"], key="habitacion")

if st.button("Enviar estado"):
    bridge.publish(TOPIC_CMD, {"sala": sala, "cocina": cocina, "habitacion": hab})
    st.toast("Comando enviado")

st.divider()
st.subheader("Escenas")
colA, colB, colC, colD = st.columns(4)
if colA.button("Noche"):
    bridge.publish(TOPIC_CMD, SCENES["noche"]) ; st.toast("Escena Noche")
if colB.button("Trabajo"):
    bridge.publish(TOPIC_CMD, SCENES["trabajo"]) ; st.toast("Escena Trabajo")
if colC.button("Todo ON"):
    bridge.publish(TOPIC_CMD, SCENES["todo_on"]) ; st.toast("Todo ON")
if colD.button("Todo OFF"):
    bridge.publish(TOPIC_CMD, SCENES["todo_off"]) ; st.toast("Todo OFF")

st.caption("Estado reciente: " + str(st.session_state.state))
