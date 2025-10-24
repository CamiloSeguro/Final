import json, os, glob
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="VR Analytics", page_icon="🎛️", layout="wide")
st.title("🎛️ VR Analytics — Sesiones y Acciones")

log_dir = st.text_input("Carpeta de logs", value="./logs_extraidos_del_quest")
files = sorted(glob.glob(os.path.join(log_dir, "*.csv")))
if not files:
    st.warning("No se encontraron CSV. Copia tus archivos desde el Quest a esta carpeta.")
    st.stop()

# Cargar múltiples sesiones
dfs = []
for f in files:
    df = pd.read_csv(f)
    try:
        # Expandir details_json a columnas
        details = df["details_json"].apply(lambda s: json.loads(s) if isinstance(s, str) else {})
        details_df = pd.json_normalize(details)
        df = pd.concat([df.drop(columns=["details_json"]), details_df], axis=1)
    except Exception:
        pass
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# Filtros
sessions = sorted(data["session_id"].unique())
sel_sessions = st.multiselect("Sesiones", sessions, default=sessions[-3:] if len(sessions)>3 else sessions)

subset = data[data["session_id"].isin(sel_sessions)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sesiones", subset["session_id"].nunique())
col2.metric("Eventos", len(subset))
t0 = subset.groupby("session_id")["elapsed_s"].min().min() if not subset.empty else 0
t1 = subset.groupby("session_id")["elapsed_s"].max().max() if not subset.empty else 0
col3.metric("Duración máx (s)", f"{t1:.1f}")
col4.metric("Variantes usadas", subset[subset["action"]=="variant_applied"]["name"].nunique())

# Timeline
st.subheader("Timeline de eventos")
st.dataframe(subset.sort_values(["session_id","elapsed_s"]))

# Uso de variantes
st.subheader("Uso de variantes")
var_counts = subset[subset["action"]=="variant_applied"]["name"].value_counts()
st.bar_chart(var_counts)

# Interacciones
st.subheader("Grabs por objeto")
grab = subset[subset["action"].isin(["grab_begin","grab_end"])]
if "object" in grab:
    st.bar_chart(grab["object"].value_counts())
else:
    st.info("No hay columna 'object' en los eventos de grab.")

# Heat de locomoción (simple por eje Z)
st.subheader("Distribución de posiciones (HMD z)")
if {"hmd_z"} <= set(subset.columns):
    st.line_chart(subset.dropna(subset=["hmd_z"]).groupby("session_id")["hmd_z"].mean())
else:
    st.info("Aún no se registran posiciones de HMD en locomotion_end.")
