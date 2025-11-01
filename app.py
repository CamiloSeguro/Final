import streamlit as st
from utils import current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")

st.markdown("""
<style>
/* Navbar superior */
.navbar {display:flex; gap:10px; align-items:center; margin:8px 0 18px}
.navbtn {padding:8px 12px; border-radius:12px; border:1px solid #E5E7EB; background:#fff; font-weight:600; text-decoration:none; color:#1F2937;}
.navbtn:hover {border-color:#c7c9d1}
.hero {padding:18px 22px; border-radius:16px; background:#fff; border:1px solid #E5E7EB;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar">', unsafe_allow_html=True)
try:
    st.page_link("pages/1_Control.py", label="🏠 Dashboard", icon=None)
    st.page_link("pages/2_Voz_y_Texto.py", label="🎙️ Voz & Texto", icon=None)
except Exception:
    st.write("Usa el menú lateral para navegar.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown("### 💡 SmartLight — Control de luces Multimodal")
st.write(
    "- Dashboard estilo **smart home**: luces por habitación, dispositivos y métricas.\n"
    "- **Voz & Texto**: comandos naturales (\"encender sala\", \"escena noche\").\n"
)
st.caption(f"MQTT broker actual: `{current_broker()}`")
st.markdown('</div>', unsafe_allow_html=True)
