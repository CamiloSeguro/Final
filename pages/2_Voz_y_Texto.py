import streamlit as st
from streamlit_mic_recorder import mic_recorder
from mqtt_client import MqttBridge
from utils import parse_command, inject_css

TOPIC_CMD = "eafit/camilo/smartlight/commands"
inject_css(st)

bridge = st.session_state.get("_bridge")
if bridge is None:
    bridge = MqttBridge(client_id="smartlight_ui")
    bridge.connect()
    st.session_state._bridge = bridge

st.markdown("## 🎙️ Voz & Texto")
st.markdown('<div class="card">', unsafe_allow_html=True)

result = mic_recorder(
    start_prompt="Di: 'encender sala', 'apagar cocina', 'escena noche'",
    just_once=True, use_container_width=True, key="mic"
)
text = st.text_input("Comando reconocido o escrito:",
                     value=(result.get("text") if isinstance(result, dict) else ""))

st.write("Ejemplos rápidos:")
cols = st.columns(4)
examples = ["encender sala", "apagar cocina", "escena noche", "encender todo"]
for i, ex in enumerate(examples):
    with cols[i]:
        if st.button(ex.title(), key=f"chip_{i}"):
            text = ex

payload = parse_command(text)
st.write("**Vista previa → payload MQTT**")
st.code(payload or {"info": "Usa micrófono o escribe un comando."}, language="json")

if st.button("🚀 Enviar"):
    if payload:
        bridge.publish(TOPIC_CMD, payload); st.success(f"Enviado: {payload}")
    else:
        st.warning("Prueba: 'encender sala' / 'apagar cocina' / 'escena trabajo'")
st.markdown('</div>', unsafe_allow_html=True)
