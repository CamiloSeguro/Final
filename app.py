import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
inject_css(st)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown("### 💡 SmartLight — Control de luces Multimodal")
st.write(
    "- **Control**: toggles y **escenas** (Noche, Trabajo, Todo ON/OFF).\n"
    "- **Voz & Texto**: comandos naturales (\"encender sala\", \"escena noche\").\n"
)
c1, c2 = st.columns(2)
with c1:
    try: st.page_link("pages/1_Control.py", label="Ir a Control 💡")
    except: st.caption("Abre **Control** desde el menú lateral.")
with c2:
    try: st.page_link("pages/2_Voz_y_Texto.py", label="Ir a Voz & Texto 🎙️")
    except: st.caption("Abre **Voz & Texto** desde el menú lateral.")
st.caption(f"Broker MQTT: `{current_broker()}`")
st.markdown('</div>', unsafe_allow_html=True)
