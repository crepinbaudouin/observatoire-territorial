# app.py - version corrigée

import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ─── COULEURS (à mettre TOUT EN HAUT) ──────────────────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"
BLACK = "#000000"
DARK_GRAY = "#1A1F2E"
LIGHT_GRAY = "#E0E0E0"
WHITE = "#FFFFFF"

# ─── CONFIG ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── FOND D'ÉCRAN ───────────────────────────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{fond_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(26, 31, 46, 0.78);
            z-index: -1;
        }}
    </style>
""", unsafe_allow_html=True)

# ─── CSS KPI ────────────────────────────────────────────────────────────────────
st.markdown(f"""
    <style>
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }}
        .kpi-hex {{
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(16px);
            border: 3px solid {VIOLET};
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            padding: 40px 24px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            transition: all 0.4s;
        }}
        .kpi-hex:hover {{
            transform: scale(1.08);
            border-color: {YELLOW};
            box-shadow: 0 20px 60px rgba(253, 209, 0, 0.5);
        }}
        .kpi-number {{
            font-size: 4.2rem;
            font-weight: 900;
            color: {ACCENT_YELLOW};
            margin: 16px 0;
            text-shadow: 0 0 25px rgba(255, 224, 102, 0.7);
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.title("Paris-Saclay")
st.sidebar.image("logo_paris_saclay.png", width=220)

page = st.sidebar.radio("Thématiques", [
    "Accueil",
    "Population",
    "Emploi / Chômage",
    "Économie",
    "Social / Ménages",
    "Santé",
    "Éducation",
    "Sports",
    "Finance (restreint)"
])

# ─── Compteur animé ─────────────────────────────────────────────────────────────
def animated_counter(label, final_value, delta="", color=YELLOW, duration=2.0):
    placeholder = st.empty()
    start = time.time()
    value = 0
    final_value = float(final_value)
    while time.time() - start < duration:
        progress = (time.time() - start) / duration
        current = int(final_value * progress)
        placeholder.markdown(f"""
        <div class="kpi-hex" style="border-color:{color};">
            <h3 style="color:{color};">{label}</h3>
            <div class="kpi-number" style="color:{color};">{current:,}</div>
            <p style="color:#E0E0E0;">{delta}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)
    placeholder.markdown(f"""
    <div class="kpi-hex" style="border-color:{color};">
        <h3 style="color:{color};">{label}</h3>
        <div class="kpi-number" style="color:{color};">{int(final_value):,}</div>
        <p style="color:#E0E0E0;">{delta}</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Accueil ────────────────────────────────────────────────────────────────────
if page == "Accueil":
    st.title("Observatoire Territorial Paris-Saclay")

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(5)

    with cols[0]:
        animated_counter("Population totale", 785420, "+2.8 %", YELLOW)

    with cols[1]:
        animated_counter("Emplois tech & R&D", 142000, "+19 %", VIOLET)

    with cols[2]:
        animated_counter("Startups actives", 1620, "14 licornes", YELLOW)

    with cols[3]:
        animated_counter("Satisfaction résidents", 86.4, "2025", VIOLET)

    with cols[4]:
        animated_counter("Investissements R&D", 3800000000, "cumulé", YELLOW)

    st.markdown("</div>", unsafe_allow_html=True)

# ─── Population ─────────────────────────────────────────────────────────────────
elif page == "Population":
    st.title("Population")

    recensement = load_data("POP_RECENSEMENT.csv")

    if not recensement.empty:
        # ... (ton code filtres et KPI Population ici)
        # Exemple simplifié pour tester
        st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            animated_counter("Population totale", 785420, "2024", YELLOW)
        with cols[1]:
            animated_counter("Moins de 20 ans", 145000, "jeunes", VIOLET)
        with cols[2]:
            animated_counter("65 ans et plus", 98000, "seniors", YELLOW)
        with cols[3]:
            animated_counter("Croissance récente", 28, "+2.8 %", VIOLET)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#888; margin:120px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Déployé via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
