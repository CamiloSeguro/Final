import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
inject_css(st)

# Tres columnas: izquierda / centro / derecha
left, center, right = st.columns([1, 4, 1])

with center:
    with st.container(border=True):
        st.markdown(
            """
            <h3 style="text-align:center;margin-top:0;">💡 SmartLight — Control de luces Multimodal</h3>
            <p style="text-align:center;opacity:.85;margin-top:.25rem;">
              Proyecto que combina control digital y físico a través de <b>interfaces multimodales</b>.<br>
              Usa texto, voz y toggles para controlar luces conectadas vía MQTT y ESP32 (Wokwi).
            </p>
            <hr style="opacity:.15;margin:.5rem 0 1rem 0;">
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            st.page_link("pages/1_Control.py", label="Ir a Control 💡")
        with c2:
            st.page_link("pages/2_Voz_y_Texto.py", label="Ir a Voz & Texto 🎙️")

        st.markdown(
            f"""
            <p style="margin-top:10px; text-align:center;">
              <b>Broker MQTT:</b> <code style="color:#22c55e;">{current_broker()}</code>
            </p>
            """,
            unsafe_allow_html=True,
        )

# Footer centrado
st.markdown(
    """
    <br><hr style="opacity:.15; margin-top:2rem; margin-bottom:1rem;">
    <div style="text-align:center; opacity:.7; font-size:13px;">
      Proyecto académico · <b>Universidad EAFIT</b> · Desarrollado por <b>Camilo Seguro Carvajal</b>
    </div>
    """,
    unsafe_allow_html=True,
)
