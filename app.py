import streamlit as st
from utils import inject_style, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")

# Sidebar: Blueprint toggle
bp = st.sidebar.toggle("🔷 Blueprint mode", value=False, help="Modo azul técnico con grid más marcado")
st.sidebar.caption(f"MQTT broker: `{current_broker()}`")

# CSS Pro
st.markdown(inject_style(blueprint=bp), unsafe_allow_html=True)

# Navbar con enlaces directos (y fallback si Streamlit no encuentra page_link)
st.markdown('<div class="navbar">', unsafe_allow_html=True)
try:
    st.page_link("pages/1_Control.py", label="💡 Control", icon=None)
    st.page_link("pages/2_Voz_y_Texto.py", label="🎙️ Voz & Texto", icon=None)
except Exception:
    st.markdown('<a class="navbtn" href="#">💡 Abre Control desde el menú</a>', unsafe_allow_html=True)
    st.markdown('<a class="navbtn" href="#">🎙️ Abre Voz & Texto desde el menú</a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Hero
c1, c2 = st.columns([3,2])
with c1:
    st.markdown("## 💡 SmartLight — Control de luces Multimodal")
    st.write(
        "- Controla **Sala**, **Cocina** y **Habitación** por **MQTT** (ESP32 en **Wokwi**).\n"
        "- **Control**: toggles y **escenas** (Noche, Trabajo, Todo ON/OFF).\n"
        "- **Voz & Texto**: comandos naturales (\"encender sala\", \"escena noche\")."
    )
with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Cómo presentar (pitch)**")
    st.caption("1) Problema → 2) Solución → 3) Demo → 4) Valor → 5) Roadmap")
    st.markdown('</div>', unsafe_allow_html=True)

st.info("Usa el menú de la izquierda o la barra superior para navegar.")
