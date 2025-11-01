import streamlit as st
from streamlit_mic_recorder import mic_recorder
from mqtt_client import MqttBridge
from utils import parse_command, inject_css

TOPIC_CMD = "eafit/camilo/smartlight/commands"

# Estilo global (set_page_config queda solo en app.py)
inject_css(st)

# Reusar puente MQTT creado en la otra página si existe
bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge

st.title("🎙️ Voz & Texto")

with st.container(border=True):
    st.subheader("Comando por voz")
    result = mic_recorder(
        start_prompt="Di: 'encender sala', 'apagar cocina', 'escena noche'",
        just_once=True, use_container_width=True, key="mic"
    )

with st.container(border=True):
    st.subheader("Comando por texto")
    text = st.text_input(
        "Escribe un comando:",
        value=(result.get("text") if isinstance(result, dict) else "")
    )

st.write("Ejemplos rápidos:")
c1, c2, c3, c4 = st.columns(4)
if c1.button("Encender sala", use_container_width=True): text = "encender sala"
if c2.button("Apagar cocina", use_container_width=True): text = "apagar cocina"
if c3.button("Escena noche", use_container_width=True):  text = "escena noche"
if c4.button("Encender todo", use_container_width=True): text = "encender todo"

payload = parse_command(text)
st.write("**Vista previa → payload MQTT**")
st.code(payload or {"info": "Usa micrófono o escribe un comando."}, language="json")

st.divider()
if st.button("🚀 Enviar", type="primary", use_container_width=True):
    if payload:
        bridge.publish(TOPIC_CMD, payload)
        st.success(f"Enviado: {payload}")
    else:
        st.warning("No entendí el comando. Prueba: 'encender sala' / 'apagar cocina' / 'escena trabajo'")

st.caption("Tip: Si el micrófono no reconoce, usa el campo de texto. Igual cuenta como multimodal.")
