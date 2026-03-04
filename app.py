# app.py - Observatoire Territorial Paris-Saclay - Style Taipy / Glassmorphism 2026
import streamlit as st
import pandas as pd
import time
import random  # pour simuler des données dynamiques

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Toggle Dark / Light ────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode, key="dark_toggle")
if dark_light != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_light
    st.rerun()

# ─── Thèmes couleurs ────────────────────────────────────────────────────────────
if st.session_state.dark_mode:
    BG = "#0f172a"
    CARD_BG = "rgba(30, 41, 59, 0.88)"
    TEXT = "#e2e8f0"
    ACCENT = "#FDD100"
    SECONDARY = "#9F7AEA"
    BORDER = "#6A1B9A"
else:
    BG = "#f8fafc"
    CARD_BG = "rgba(255, 255, 255, 0.92)"
    TEXT = "#0f172a"
    ACCENT = "#F59E0B"
    SECONDARY = "#7C3AED"
    BORDER = "#6D28D9"

# ─── Fond + style glassmorphism ─────────────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{fond_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: {TEXT};
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: {BG};
            opacity: 0.82;
            z-index: -1;
        }}
        .header {{
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255,255,255,0.12);
            padding: 16px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .logo-title h1 {{
            margin: 0;
            font-size: 2.4rem;
            background: linear-gradient(90deg, {ACCENT}, {SECONDARY});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .tabs-container {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
            margin: 24px 0 40px;
        }}
        .tab-btn {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 50px;
            padding: 12px 28px;
            color: white;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .tab-btn:hover {{
            background: rgba(253,209,0,0.15);
            transform: translateY(-2px);
        }}
        .tab-btn.active {{
            background: linear-gradient(45deg, {VIOLET}, {SECONDARY});
            box-shadow: 0 8px 25px rgba(106,27,154,0.4);
        }}
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 28px;
            margin: 40px 0;
        }}
        .kpi-card {{
            background: {CARD_BG};
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            transition: transform 0.3s;
        }}
        .kpi-card:hover {{
            transform: translateY(-8px);
        }}
        .kpi-title {{
            font-size: 1.3rem;
            color: #94a3b8;
            margin-bottom: 12px;
        }}
        .kpi-value {{
            font-size: 3.2rem;
            font-weight: 800;
            color: {ACCENT};
            margin: 8px 0;
        }}
        .kpi-delta {{
            font-size: 1.1rem;
            color: #10b981;
        }}
        .login-card {{
            background: {CARD_BG};
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px;
            max-width: 420px;
            margin: 60px auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }}
        .login-input {{
            width: 100%;
            padding: 14px;
            margin: 12px 0;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(255,255,255,0.06);
            color: white;
        }}
        .login-btn {{
            width: 100%;
            padding: 16px;
            background: linear-gradient(45deg, {VIOLET}, {SECONDARY});
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }}
        @media (max-width: 768px) {{
            .kpi-container {{
                grid-template-columns: 1fr;
            }}
            .kpi-value {{
                font-size: 2.8rem;
            }}
            .tabs-container {{
                flex-direction: column;
                align-items: center;
            }}
            .header {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Barre du haut ──────────────────────────────────────────────────────────────
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=70)

with col_title:
    st.markdown(f"""
        <h1 style="margin:0; text-align:center; font-size:2.6rem;">
            PARIS <span style="color:{YELLOW};">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#94a3b8; margin:4px 0 0;">
            Communauté d'agglomération
        </p>
    """, unsafe_allow_html=True)

with col_toggle:
    st.toggle("Dark / Light", value=st.session_state.dark_mode, key="toggle_dark")

# ─── Navigation horizontale ─────────────────────────────────────────────────────
themes = [
    ("Accueil", "🏠"),
    ("Population", "👥"),
    ("Emploi / Chômage", "💼"),
    ("Économie", "📈"),
    ("Social / Ménages", "🏡"),
    ("Santé", "🩺"),
    ("Éducation", "🎓"),
    ("Sports", "⚽"),
    ("Finance", "💰")
]

st.markdown("<div class='tabs-container'>", unsafe_allow_html=True)
selected_tab = st.radio(
    "Navigation",
    [f"{icon} {name}" for name, icon in themes],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

current_theme = selected_tab.split(" ", 1)[1]

# ─── Compteur animé ─────────────────────────────────────────────────────────────
def animated_kpi(label, value, delta="", color=ACCENT_YELLOW):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value" style="color:{color};">{value:,}</div>
        <div class="kpi-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Contenu par page ───────────────────────────────────────────────────────────
st.markdown("<div class='main'>", unsafe_allow_html=True)

if current_theme == "Accueil":
    st.markdown("<h1 style='text-align:center; margin-bottom:40px;'>Bienvenue sur l'Observatoire</h1>")
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        animated_kpi("Population", 785420, "+2.8 %")
    with col2:
        animated_kpi("Emplois", 142000, "+19 %")
    with col3:
        animated_kpi("Startups", 1620, "14 licornes")
    with col4:
        animated_kpi("Satisfaction", "86.4 %", "2025")
    st.markdown("</div>", unsafe_allow_html=True)

elif current_theme == "Finance":
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#FDD100; text-align:center;'>Finance</h2>")
    st.text_input("Identifiant")
    st.text_input("Mot de passe", type="password")
    if st.button("Se connecter", type="primary", use_container_width=True):
        st.success("Connexion simulée réussie")
    st.markdown("<p style='text-align:center; margin-top:20px; color:#94a3b8;'>Mot de passe oublié ?</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"<h2 style='text-align:center;'>{current_theme}</h2>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            animated_kpi(f"Indicateur {i+1}", random.randint(1000, 50000), "+X %")
    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Contenu détaillé {current_theme} en cours de développement")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; color:#94a3b8; margin:100px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Développé avec Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
