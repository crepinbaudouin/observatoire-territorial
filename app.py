# app.py - Observatoire Territorial Paris-Saclay - Version améliorée 2026
import streamlit as st
import pandas as pd
import time

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed sur mobile
)

# ─── État dark/light ────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ─── Couleurs charte ────────────────────────────────────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"
BG_DARK = "#0f172a"
BG_LIGHT = "#f8fafc"
CARD_DARK = "rgba(30, 41, 59, 0.88)"
CARD_LIGHT = "rgba(255, 255, 255, 0.92)"

# ─── Fond + style global ────────────────────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

bg_color = BG_DARK if st.session_state.dark_mode else BG_LIGHT
card_bg = CARD_DARK if st.session_state.dark_mode else CARD_LIGHT
text_color = "#ffffff" if st.session_state.dark_mode else "#0f172a"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{fond_url}");
            background-size: cover;
            background-position: center;
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
        .main {{
            color: {text_color};
            padding: 20px 40px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 40px;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .logo-title {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .logo-title h1 {{
            margin: 0;
            font-size: 2.2rem;
            background: linear-gradient(90deg, {YELLOW}, {ACCENT_VIOLET});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .nav-tabs {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
            margin: 30px 0;
        }}
        .nav-tab {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
            border-radius: 50px;
            padding: 12px 28px;
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-tab:hover, .nav-tab.active {{
            background: linear-gradient(45deg, {VIOLET}, {ACCENT_VIOLET});
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(106,27,154,0.4);
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
            border: 2px solid {VIOLET};
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            padding: 40px 24px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: all 0.4s;
        }}
        .kpi-hex:hover {{
            transform: scale(1.08);
            border-color: {YELLOW};
            box-shadow: 0 20px 60px rgba(253, 209, 0, 0.4);
        }}
        .kpi-number {{
            font-size: 4.2rem;
            font-weight: 900;
            color: {ACCENT_YELLOW};
            margin: 16px 0;
            text-shadow: 0 0 25px rgba(255, 224, 102, 0.7);
        }}
        @media (max-width: 768px) {{
            .header {{
                flex-direction: column;
                gap: 15px;
                padding: 15px 20px;
            }}
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            .kpi-number {{
                font-size: 3.2rem;
            }}
            .nav-tabs {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Barre du haut ──────────────────────────────────────────────────────────────
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=80)

with col_title:
    st.markdown("""
        <h1 style="margin:0; text-align:center;">
            PARIS <span style="color:#FDD100;">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#ccc; margin:4px 0 0;">
            Communauté d'agglomération
        </p>
    """, unsafe_allow_html=True)

with col_toggle:
    dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode)
    if dark_light != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_light
        st.rerun()

# ─── Navigation horizontale avec icônes ─────────────────────────────────────────
themes = [
    ("Accueil", "🏠"),
    ("Population", "👥"),
    ("Emploi / Chômage", "💼"),
    ("Économie", "📈"),
    ("Social / Ménages", "🏡"),
    ("Santé", "🩺"),
    ("Éducation", "🎓"),
    ("Sports", "⚽"),
    ("Finance (restreint)", "💰")
]

st.markdown("<div class='nav-tabs'>", unsafe_allow_html=True)
selected_index = st.radio(" ", [f"{icon} {name}" for name, icon in themes], horizontal=True, key="nav")
st.markdown("</div>", unsafe_allow_html=True)

selected_theme = themes[[f"{icon} {name}" for name, icon in themes].index(selected_index)][0]

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

# ─── Contenu par page ───────────────────────────────────────────────────────────
st.markdown("<div class='main'>", unsafe_allow_html=True)

if selected_theme == "Accueil":
    st.markdown("<h1 style='text-align:center; color:#FDD100;'>Bienvenue</h1>")
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

elif selected_theme == "Population":
    st.subheader("Filtres")
    col1, col2 = st.columns(2)
    with col1:
        annee = st.selectbox("Année", ["2024", "2023", "2022"])
    with col2:
        commune = st.selectbox("Commune", ["Toutes", "Massy", "Orsay", "Palaiseau"])

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        animated_counter("Population totale", 785420, f"{annee}", YELLOW)
    with cols[1]:
        animated_counter("Moins de 20 ans", 145000, "jeunes", VIOLET)
    with cols[2]:
        animated_counter("65 ans et plus", 98000, "seniors", YELLOW)
    with cols[3]:
        animated_counter("Solde naturel", 3200, "naissances - décès", VIOLET)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"<h2>{selected_theme}</h2>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            animated_counter(f"Indicateur {i+1}", 12345 + i*5000, "2025", YELLOW if i%2==0 else VIOLET)
    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Contenu {selected_theme} en cours de développement")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; color:#aaa; margin-top:80px; padding:20px;">
    © Communauté Paris-Saclay | Données 2026 | Développé avec ❤️
</div>
""", unsafe_allow_html=True)
