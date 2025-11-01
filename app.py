import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")

inject_css(st)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown("### 💡 SmartLight — Control de luces Multimodal")
st.write(
    "- Controla **Sala**, **Cocina** y **Habitación** conectadas por **MQTT** a un ESP32 en **Wokwi**.\n"
    "- **Control**: toggles y **escenas** (Noche, Trabajo, Todo ON/OFF).\n"
    "- **Voz & Texto**: comandos naturales (\"encender sala\", \"escena noche\")."
)
c1, c2, c3 = st.columns([1,1,2])
with c1:
    # Enlaces nativos a páginas
    try:
        st.page_link("pages/1_Control.py", label="Ir a Control", icon="💡")
    except Exception:
        st.write("💡 Abre el menú lateral y entra a **Control**.")
with c2:
    try:
        st.page_link("pages/2_Voz_y_Texto.py", label="Ir a Voz & Texto", icon="🎙️")
    except Exception:
        st.write("🎙️ Abre **Voz & Texto** desde el menú lateral.")
with c3:
    st.caption(f"Broker MQTT actual: `{current_broker()}`")
st.markdown('</div>', unsafe_allow_html=True)

st.info("Usa el menú de la izquierda o los enlaces para navegar.")
