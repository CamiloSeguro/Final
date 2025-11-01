import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
inject_css(st)

hero_html = f"""
<div class="hero">
  <h3>💡 SmartLight — Control de luces Multimodal</h3>
  <ul>
    <li><b>Control</b>: toggles y <b>escenas</b> (Noche, Trabajo, Todo ON/OFF).</li>
    <li><b>Voz & Texto</b>: comandos naturales ("encender sala", "escena noche").</li>
  </ul>
  <div style="display:flex; gap:24px; margin-top:8px;">
    <a href="pages/1_Control.py">Ir a Control 💡</a>
    <a href="pages/2_Voz_y_Texto.py">Ir a Voz & Texto 🎙️</a>
  </div>
  <p style="margin-top:8px;">Broker MQTT: <code>{current_broker()}</code></p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)
