# app.py - Observatoire Territorial Paris-Saclay
# Version avec chargement direct depuis GitHub + indicateurs Population

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Config page ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS waouh (glassmorphism + glow + dark mode) ───────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.7);
        --text: #e2e8f0;
        --accent: #3b82f6;
        --glow: 0 0 30px rgba(59, 130, 246, 0.6);
    }

    body, .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .hero {
        height: 80vh;
        background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.9)),
                    url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 0 0 32px 32px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
    }

    .hero h1 {
        font-size: 5rem;
        font-weight: 900;
        text-shadow: 0 6px 30px rgba(0,0,0,0.8);
        background: linear-gradient(90deg, #60a5fa, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 6s ease-in-out infinite alternate;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 20px rgba(96, 165, 250, 0.8); }
        100% { text-shadow: 0 0 70px rgba(165, 180, 252, 1); }
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 32px;
        margin: 60px 0;
    }

    .kpi-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 28px;
        padding: 36px;
        text-align: center;
        transition: all 0.5s;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
    }

    .kpi-card:hover {
        transform: translateY(-16px);
        box-shadow: 0 40px 100px rgba(59, 130, 246, 0.4);
    }

    .kpi-number {
        font-size: 4rem;
        font-weight: 900;
        color: #60a5fa;
        margin: 16px 0;
    }

    .sidebar .sidebar-content {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(16px) !important;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ─── Hero section ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <h1>Observatoire Territorial</h1>
        <p style="font-size:1.8rem; margin:2rem 0; max-width:900px;">
            Indicateurs clés en temps réel – Agglomération Paris-Saclay
        </p>
        <div>
            <a href="#population" class="btn-glow" style="text-decoration:none;">Découvrir les données</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.title("Observatoire Paris-Saclay")
st.sidebar.image("logo_paris_saclay.png", width=180)  # fichier à la racine

# ─── Chargement données depuis GitHub raw ───────────────────────────────────────
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        return pd.read_csv(url, sep=";", decimal=",", low_memory=False)
    except Exception as e:
        st.error(f"Erreur chargement {file_name} : {e}")
        return pd.DataFrame()

# ─── Page Accueil ───────────────────────────────────────────────────────────────
st.title("Accueil – Observatoire Territorial Paris-Saclay")

# Exemples d’indicateurs fictifs (à remplacer par tes données réelles)
kpi_data = {
    "Population totale": "785 420 hab.",
    "Croissance annuelle": "+2.8 %",
    "Emplois tech / R&D": "142 000",
    "Startups actives": "1 620",
    "Satisfaction résidents": "86.4 %"
}

cols = st.columns(5)
for col, (label, value) in zip(cols, kpi_data.items()):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>{label}</h3>
            <div class="kpi-number">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Section Population (premier exemple avec vrai CSV) ────────────────────────
st.header("Population – Indicateurs clés")

pop_df = load_data("POP_RECENSEMENT.csv")

if not pop_df.empty:
    # Nettoyage léger des colonnes
    pop_df = pop_df.rename(columns=lambda x: x.strip())
    if "Valeur" in pop_df.columns:
        pop_df["Valeur"] = pd.to_numeric(pop_df["Valeur"], errors="coerce")

    # Indicateur 1 : Population totale par période (agrégation simple)
    st.subheader("Population totale par période")
    total_pop = pop_df[pop_df["Âge"] == "Total"].groupby("Période")["Valeur"].sum().reset_index()
    fig_pop = px.line(total_pop, x="Période", y="Valeur", title="Évolution population totale")
    st.plotly_chart(fig_pop, use_container_width=True)

    # Indicateur 2 : Répartition par sexe (exemple)
    st.subheader("Répartition par sexe (dernière période)")
    last_period = pop_df["Période"].max()
    sex_df = pop_df[(pop_df["Période"] == last_period) & (pop_df["Sexe"] != "Total")]
    fig_sex = px.pie(sex_df, values="Valeur", names="Sexe", title=f"Répartition par sexe en {last_period}")
    st.plotly_chart(fig_sex, use_container_width=True)

    # Tableau brut (extrait)
    st.subheader("Extrait des données brutes")
    st.dataframe(pop_df.head(10))
else:
    st.warning("Impossible de charger POP_RECENSEMENT.csv depuis GitHub")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#64748b; margin:120px 0 40px;">
    © Communauté Paris-Saclay | Données février 2026 | App déployée via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
