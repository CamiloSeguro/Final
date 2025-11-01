import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
inject_css(st)

st.markdown("""
<div class="hero">
  <h3>💡 SmartLight — Control de luces Multimodal</h3>
  <ul>
    <li><b>Control</b>: toggles y <b>escenas</b> (Noche, Trabajo, Todo ON/OFF).</li>
    <li><b>Voz & Texto</b>: comandos naturales como "encender sala" o "escena noche".</li>
  </ul>
  <div style="display:flex; gap:24px; margin-top:8px; flex-wrap:wrap;">
    <a href="pages/1_Control.py" style="text-decoration:none; font-weight:600;">Ir a Control 💡</a>
    <a href="pages/2_Voz_y_Texto.py" style="text-decoration:none; font-weight:600;">Ir a Voz & Texto 🎙️</a>
  </div>
  <p style="margin-top:10px;">
    <b>Broker MQTT:</b> <code style="color:#22c55e;">""" + current_broker() + """</code>
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<hr style="opacity:.15; margin-top:2rem; margin-bottom:1rem;">
<div style="text-align:center; opacity:.7; font-size:13px;">
  Proyecto académico · Universidad EAFIT · Desarrollado por <b>Camilo Seguro Carvajal</b>
</div>
""", unsafe_allow_html=True)
