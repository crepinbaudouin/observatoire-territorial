# utils.py
import streamlit as st
import pandas as pd
import plotly.express as px

YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"
BG_DARK = "#0f172a"
BG_LIGHT = "#f8fafc"
CARD_DARK = "rgba(30, 41, 59, 0.88)"
CARD_LIGHT = "rgba(255, 255, 255, 0.92)"

def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        return pd.read_csv(url, sep=";", decimal=",", low_memory=False)
    except:
        return pd.DataFrame()

def animated_kpi(label, value, delta="", color=ACCENT_YELLOW):
    st.markdown(f"""
    <div style="
        background: {CARD_DARK if st.session_state.get('dark_mode', True) else CARD_LIGHT};
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.25);
        text-align: center;
    ">
        <div style="font-size:1.3rem; color:#94a3b8; margin-bottom:12px;">{label}</div>
        <div style="font-size:3.2rem; font-weight:800; color:{color};">{value}</div>
        <div style="font-size:1.1rem; color:#10b981;">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

def get_theme_css():
    dark = st.session_state.get('dark_mode', True)
    bg = BG_DARK if dark else BG_LIGHT
    card = CARD_DARK if dark else CARD_LIGHT
    text = "#ffffff" if dark else "#0f172a"
    return f"""
        .stApp::before {{
            background: {bg};
            opacity: 0.82;
        }}
        h1, h2, h3, p {{
            color: {text} !important;
        }}
    """
