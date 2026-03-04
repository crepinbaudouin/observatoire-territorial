# app.py
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from pathlib import Path
import base64
import pandas as pd

# ─── Config page ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Dark mode + custom CSS (glassmorphism + glow + animations) ────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.6);
        --text: #e2e8f0;
        --accent: #3b82f6;
        --accent-dark: #2563eb;
        --glow: 0 0 30px rgba(59, 130, 246, 0.5);
    }

    body, .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .hero {
        position: relative;
        height: 85vh;
        background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.85)),
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
        font-size: 4.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.6);
        background: linear-gradient(90deg, #60a5fa, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }

    @keyframes titleGlow {
        0% { text-shadow: 0 0 20px rgba(96, 165, 250, 0.6); }
        100% { text-shadow: 0 0 50px rgba(165, 180, 252, 0.9); }
    }

    .hero-subtitle {
        font-size: 1.6rem;
        margin: 1.5rem 0 2.5rem;
        opacity: 0.9;
        max-width: 800px;
    }

    .btn-glow {
        background: var(--accent);
        color: white;
        padding: 16px 40px;
        font-size: 1.3rem;
        font-weight: 600;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.35s;
        box-shadow: var(--glow);
        margin: 0 12px;
    }

    .btn-glow:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 0 60px rgba(59, 130, 246, 0.8);
        background: var(--accent-dark);
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 28px;
        margin: 60px 0;
    }

    .kpi-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.4s;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }

    .kpi-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3);
    }

    .kpi-number {
        font-size: 3.8rem;
        font-weight: 800;
        color: #60a5fa;
        margin: 12px 0;
    }

    .sidebar .sidebar-content {
        background: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(12px) !important;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ─── Hero banner (image statique pour démarrer – vidéo plus bas si besoin) ────────
with st.container():
    st.markdown("""
    <div class="hero">
        <div>
            <h1>Observatoire Territorial</h1>
            <p class="hero-subtitle">
                Suivi en temps réel des indicateurs clés de l’agglomération Paris-Saclay<br>
                Données fiables · Analyses avancées · Décision stratégique
            </p>
            <div>
                <button class="btn-glow">Explorer les indicateurs</button>
                <button class="btn-glow" style="background:transparent; border:2px solid #64748b;">
                    Accès Finance (restreint)
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── KPI cards (exemples fictifs – à brancher sur tes CSV plus tard) ─────────────
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
        <h3>Emplois tech & R&D</h3>
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
        <h3>Satisfaction résidents</h3>
        <div class="kpi-number">86,4 %</div>
        <p style="color:#94a3b8;">(enquête 2025)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Sidebar (thèmes) ───────────────────────────────────────────────────────────
st.sidebar.title("Observatoire Paris-Saclay")
st.sidebar.image("assets/images/logo_paris_saclay.png", width=180)

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

if choice != "Accueil":
    st.title(choice)
    st.info(f"Page {choice} en construction – indicateurs à venir")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#64748b; margin:80px 0 40px;">
    © Communauté Paris-Saclay | Données actualisées février 2026
</div>
""", unsafe_allow_html=True)
