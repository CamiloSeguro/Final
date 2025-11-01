import streamlit as st
st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")

st.title("SmartLight — Control de luces Multimodal")
st.markdown(
    """
    Controla **Sala**, **Cocina** y **Habitación** conectadas por **MQTT** a un ESP32 en **Wokwi**.
    - Página **Control**: toggles y **escenas** (Noche, Trabajo, Todo ON/OFF).
    - Página **Voz & Texto**: instrucciones naturales como “encender sala” o “escena noche”.
    """
)

st.success("Usa el menú de la izquierda para navegar.")
