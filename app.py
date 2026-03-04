# app.py - Observatoire Territorial Paris-Saclay - Navigation horizontale + responsive + dark/light
import streamlit as st
import pandas as pd
import time

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"   # Collapsed par défaut sur mobile
)

# ─── État pour dark/light ───────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ─── Fond d'écran (ajusté selon mode) ──────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

bg_color = "#0f172a" if st.session_state.dark_mode else "#f8fafc"
text_color = "#ffffff" if st.session_state.dark_mode else "#0f172a"
card_bg = "rgba(30, 41, 59, 0.85)" if st.session_state.dark_mode else "rgba(255,255,255,0.92)"

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
            background: {bg_color};
            opacity: 0.82;
            z-index: -1;
        }}
        .main-content {{
            color: {text_color};
            padding: 20px 40px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }}
        .kpi-hex {{
            background: {card_bg};
            backdrop-filter: blur(16px);
            border: 2px solid #6A1B9A;
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            padding: 40px 24px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: all 0.4s;
        }}
        .kpi-hex:hover {{
            transform: scale(1.08);
            border-color: #FDD100;
            box-shadow: 0 20px 60px rgba(253, 209, 0, 0.4);
        }}
        .kpi-number {{
            font-size: 4.2rem;
            font-weight: 900;
            color: #FFE066;
            margin: 16px 0;
            text-shadow: 0 0 25px rgba(255, 224, 102, 0.7);
        }}
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 8px;
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 40px;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: white !important;
            font-weight: 500;
            padding: 12px 24px !important;
            border-radius: 50px !important;
            transition: all 0.3s;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background: rgba(253,209,0,0.15) !important;
            color: #FDD100 !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(90deg, #6A1B9A, #9F7AEA) !important;
            color: white !important;
        }}
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: 1fr !important;
            }}
            .kpi-number {{
                font-size: 3.2rem !important;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                flex-wrap: wrap !important;
                justify-content: flex-start !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Barre du haut ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    st.image("logo_paris_saclay.png", width=80)

with col2:
    st.markdown("""
        <h1 style="margin:0; text-align:center; color:#FDD100; font-size:2.8rem;">
            PARIS <span style="color:#fff;">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#ccc; margin:4px 0 0;">
            Communauté d'agglomération
        </p>
    """, unsafe_allow_html=True)

with col3:
    dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode)
    if dark_light != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_light
        st.rerun()

# ─── Navigation horizontale ─────────────────────────────────────────────────────
themes = [
    "Accueil 🏠",
    "Population 👥",
    "Emploi / Chômage 💼",
    "Économie 📈",
    "Social / Ménages 🏡",
    "Santé 🩺",
    "Éducation 🎓",
    "Sports ⚽",
    "Finance (restreint) 💰"
]

selected_theme = st.tabs(themes)

# ─── Contenu selon onglet ───────────────────────────────────────────────────────
current_tab = [i for i, tab in enumerate(selected_theme) if tab.active][0]

# Fonction compteur animé
def animated_counter(label, final_value, delta="", color="#FDD100", duration=2.0):
    placeholder = st.empty()
    start = time.time()
    value = 0
    final_value = float(final_value)
    while time.time() - start < duration:
        progress = (time.time() - start) / duration
        current = int(final_value * progress)
        placeholder.markdown(f"""
        <div class="kpi-hex">
            <h3 style="color:{color};">{label}</h3>
            <div class="kpi-number" style="color:{color};">{current:,}</div>
            <p style="color:#ccc;">{delta}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)
    placeholder.markdown(f"""
    <div class="kpi-hex">
        <h3 style="color:{color};">{label}</h3>
        <div class="kpi-number" style="color:{color};">{int(final_value):,}</div>
        <p style="color:#ccc;">{delta}</p>
    </div>
    """, unsafe_allow_html=True)

# Exemple Accueil
if current_tab == 0:
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        animated_counter("Population", 785420, "+2.8 %", YELLOW)
    with cols[1]:
        animated_counter("Emplois", 142000, "+19 %", VIOLET)
    with cols[2]:
        animated_counter("Startups", 1620, "14 licornes", YELLOW)
    with cols[3]:
        animated_counter("Satisfaction", 86.4, "2025", VIOLET)
    st.markdown("</div>", unsafe_allow_html=True)

# Exemple Population (avec filtres)
elif current_tab == 1:
    st.subheader("Filtres")
    col1, col2 = st.columns(2)
    with col1:
        annee = st.selectbox("Année", ["2024", "2023", "2022"])
    with col2:
        commune = st.selectbox("Commune", ["Toutes", "Massy", "Orsay", "Palaiseau"])

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        animated_counter("Population", 785420, f"{annee}", YELLOW)
    with cols[1]:
        animated_counter("Moins de 20 ans", 145000, "jeunes", VIOLET)
    with cols[2]:
        animated_counter("65 ans et +", 98000, "seniors", YELLOW)
    with cols[3]:
        animated_counter("Solde naturel", 3200, "naissances - décès", VIOLET)
    st.markdown("</div>", unsafe_allow_html=True)

# Autres onglets (placeholders avec 4 KPI)
else:
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            animated_counter(f"Indicateur {i+1}", 12345 + i*5000, "2025", YELLOW if i%2==0 else VIOLET)
    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Contenu {themes[current_tab]} en cours de développement")

# Footer
st.markdown("""
<div style="text-align:center; color:#aaa; margin-top:80px; padding:20px;">
    © Communauté Paris-Saclay | Données 2026 | Développé avec ❤️
</div>
""", unsafe_allow_html=True)
