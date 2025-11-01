import streamlit as st
from streamlit_mic_recorder import mic_recorder
from mqtt_client import MqttBridge
from utils import parse_command

TOPIC_CMD = "eafit/camilo/smartlight/commands"

bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge

st.title("🎙️ Voz & Texto")

result = mic_recorder(
    start_prompt="Di: 'encender sala', 'apagar cocina', 'escena noche'",
    just_once=True, use_container_width=True, key="mic"
)
text = st.text_input("Comando reconocido o escrito:", value=(result.get("text") if isinstance(result, dict) else ""))

if st.button("Interpretar y enviar"):
    payload = parse_command(text)
    if payload:
        bridge.publish(TOPIC_CMD, payload)
        st.success(f"Enviado: {payload}")
    else:
        st.warning("No entendí el comando. Prueba: 'encender sala' / 'apagar cocina' / 'escena trabajo'")
