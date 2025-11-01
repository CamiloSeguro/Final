import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
inject_css(st)

# ---- Centramos todo vertical y horizontal ----
st.markdown("""
<style>
.main-container {
    height: 85vh;                       /* ocupa el alto de la ventana */
    display: flex;
    flex-direction: column;
    justify-content: center;            /* centra vertical */
    align-items: center;                /* centra horizontal */
}
.hero-box {
    width: 800px;
    padding: 28px 32px;
    border-radius: 18px;
    background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
    border: 1px solid rgba(255,255,255,.10);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown(f"""
<div class="hero-box">
    <h3>💡 SmartLight — Control de luces Multimodal</h3>
    <p style="opacity:.85;">
      Proyecto que combina control digital y físico mediante <b>interfaces multimodales</b>.<br>
      Usa texto, voz y toggles para controlar luces conectadas vía MQTT y ESP32 (Wokwi).
    </p>
    <hr style="opacity:.15; margin:.5rem 0 1rem 0;">
    <div style="display:flex; justify-content:center; gap:2rem;">
        <a href="pages/1_Control.py" style="text-decoration:none; font-weight:600;">Ir a Control 💡</a>
        <a href="pages/2_Voz_y_Texto.py" style="text-decoration:none; font-weight:600;">Ir a Voz & Texto 🎙️</a>
    </div>
    <p style="margin-top:10px;">
        <b>Broker MQTT:</b> <code style="color:#22c55e;">{current_broker()}</code>
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer ----
st.markdown("""
<hr style="opacity:.15; margin-top:2rem; margin-bottom:1rem;">
<div style="text-align:center; opacity:.7; font-size:13px;">
  Proyecto académico · <b>Universidad EAFIT</b> · Desarrollado por <b>Camilo Seguro Carvajal</b>
</div>
""", unsafe_allow_html=True)
