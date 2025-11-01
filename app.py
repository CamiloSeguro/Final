import streamlit as st
from utils import inject_css, current_broker

st.set_page_config(page_title="SmartLight", page_icon="💡", layout="wide")
def inject_css(st):
    st.markdown("""
    <style>
    /* ---- Ancho y espaciado global ---- */
    .block-container{
      padding-top: 1.2rem !important;
      padding-bottom: 2rem !important;
      max-width: 1200px;         /* <— aumenta el ancho útil */
      margin: 0 auto;
    }
    @media (min-width:1600px){
      .block-container{ max-width: 1400px; }  /* pantallas grandes */
    }

    /* ---- Estilos UI ---- */
    .hero{
      padding:18px 22px; border-radius:16px;
      background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
      border:1px solid rgba(255,255,255,.08);
    }
    .card{ padding:16px; border-radius:14px;
      background:#0e1420; border:1px solid rgba(255,255,255,.08); }
    .pill{ display:inline-flex; gap:8px; align-items:center; padding:6px 10px; border-radius:999px;
      border:1px solid rgba(255,255,255,.08); background:rgba(34,197,94,.12); font-size:13px; }
    .pill.bad{ background:rgba(239,68,68,.12); }
    .chips{ display:flex; gap:8px; flex-wrap:wrap; }
    .chip{ padding:6px 10px; border-radius:999px; font-size:12px; background:#0f172a;
      border:1px solid rgba(255,255,255,.08); cursor:pointer; }
    .primary-btn button{ width:100%; padding:10px 14px; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)

