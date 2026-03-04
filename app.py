# app.py - Version racine - logo à la racine du repo
import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Config page ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS waouh (glassmorphism + glow + animations) ──────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.65);
        --text: #e2e8f0;
        --accent: #3b82f6;
        --accent-dark: #2563eb;
        --glow: 0 0 30px rgba(59, 130, 246, 0.6);
    }

    body, .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .hero {
        position: relative;
        height: 80vh;
        background: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)),
                    url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2340&q=90');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 0 0 32px 32px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
    }

    .hero h1 {
        font-size: 5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 6px 25px rgba(0,0,0,0.7);
        background: linear-gradient(90deg, #60a5fa, #a5b4fc, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 5s ease-in-out infinite alternate;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 20px rgba(96, 165, 250, 0.7); }
        100% { text-shadow: 0 0 60px rgba(165, 180, 252, 1); }
    }

    .hero-subtitle {
        font-size: 1.8rem;
        margin: 2rem 0 3rem;
        max-width: 900px;
        opacity: 0.95;
    }

    .btn-glow {
        background: var(--accent);
        color: white;
        padding: 18px 48px;
        font-size: 1.4rem;
        font-weight: 700;
        border: none;
        border-radius: 60px;
        cursor: pointer;
        transition: all 0.4s;
        box-shadow: var(--glow);
        margin: 0 16px;
    }

    .btn-glow:hover {
        transform: translateY(-6px) scale(1.08);
        box-shadow: 0 0 80px rgba(59, 130, 246, 0.9);
        background: var(--accent-dark);
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 32px;
        margin: 70px 0;
    }

    .kpi-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 28px;
        padding: 36px 28px;
        text-align: center;
        transition: all 0.5s;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
    }

    .kpi-card:hover {
        transform: translateY(-16px);
        box-shadow: 0 40px 100px rgba(59, 130, 246, 0.4);
    }

    .kpi-number {
        font-size: 4.2rem;
        font-weight: 900;
        color: #60a5fa;
        margin: 16px 0;
    }

    .sidebar .sidebar-content {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ─── Hero banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <h1>Observatoire Territorial</h1>
        <p class="hero-subtitle">
            Suivi en temps réel – Indicateurs stratégiques – Agglomération Paris-Saclay
        </p>
        <div>
            <button class="btn-glow">Découvrir les données</button>
            <button class="btn-glow" style="background:transparent; border:2px solid #64748b;">
                Finance (accès sécurisé)
            </button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar avec logo à la racine ──────────────────────────────────────────────
try:
    st.sidebar.image("logo_paris_saclay.png", width=180)
except:
    st.sidebar.image("https://via.placeholder.com/180x180/0f172a/60a5fa?text=Paris-Saclay", width=180)
    st.sidebar.warning("Logo non trouvé – chemin racine attendu")

st.sidebar.title("Observatoire Paris-Saclay")

# Menu simple (plus tard multi-page)
themes = [
    "Accueil",
    "Population",
    "Emploi / Chômage",
    "Économie",
    "Social / Ménages",
    "Santé",
    "Éducation",
    "Sports",
    "Finance (restreint)"
]

choice = st.sidebar.radio("Navigation", themes, index=0)

# ─── KPI cards waouh ────────────────────────────────────────────────────────────
st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

cols = st.columns(4)
with cols[0]:
    st.markdown("""
    <div class="kpi-card">
        <h3>Population</h3>
        <div class="kpi-number">785 420</div>
        <p style="color:#94a3b8;">habitants (+2.8 % / an)</p>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="kpi-card">
        <h3>Emplois tech</h3>
        <div class="kpi-number">142 000</div>
        <p style="color:#94a3b8;">(+19 % en 5 ans)</p>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div class="kpi-card">
        <h3>Startups</h3>
        <div class="kpi-number">1 620</div>
        <p style="color:#94a3b8;">dont 14 licornes</p>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    st.markdown("""
    <div class="kpi-card">
        <h3>Satisfaction</h3>
        <div class="kpi-number">86,4 %</div>
        <p style="color:#94a3b8;">résidents (2025)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Contenu selon choix sidebar ────────────────────────────────────────────────
if choice == "Accueil":
    st.markdown("""
    <div style="text-align:center; margin:60px 0;">
        <h2>Bienvenue dans l'Observatoire</h2>
        <p style="font-size:1.3rem; color:#cbd5e1;">
            Sélectionnez une thématique dans la barre latérale pour explorer les indicateurs.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif choice == "Population":
    st.title("Population")
    st.info("Page en construction – Chargement des données recensement à venir...")

# Ajoute les autres choix de la même façon quand tu veux

# Footer
st.markdown("""
<div style="text-align:center; color:#64748b; margin:100px 0 40px;">
    © Communauté Paris-Saclay | Données février 2026
</div>
""", unsafe_allow_html=True)
