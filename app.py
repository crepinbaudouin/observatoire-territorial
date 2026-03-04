# app.py - Observatoire Territorial Paris-Saclay - Toutes les pages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS waouh ──────────────────────────────────────────────────────────────────
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
        height: 70vh;
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

# ─── Chargement données depuis GitHub raw ───────────────────────────────────────
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        df = pd.read_csv(url, sep=";", decimal=",", low_memory=False)
        return df
    except Exception as e:
        st.error(f"Erreur chargement {file_name} : {e}")
        return pd.DataFrame()

# ─── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.title("Observatoire Paris-Saclay")
st.sidebar.image("logo_paris_saclay.png", width=180)

page = st.sidebar.radio("Navigation", [
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

# ─── Hero (sur toutes les pages sauf Finance) ───────────────────────────────────
if page != "Finance (restreint)":
    st.markdown("""
    <div class="hero">
        <div>
            <h1>Observatoire Territorial</h1>
            <p class="hero-subtitle">
                Agglomération Paris-Saclay – Indicateurs stratégiques en temps réel
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Contenu par page ───────────────────────────────────────────────────────────
if page == "Accueil":
    st.title("Bienvenue dans l'Observatoire")
    st.markdown("""
    Cet espace permet de suivre les principaux indicateurs de l'agglomération Paris-Saclay.

    **Sélectionnez une thématique** dans la barre latérale pour explorer les données.
    """)

    # KPI fictifs (à remplacer par vrais calculs plus tard)
    cols = st.columns(4)
    cols[0].metric("Population", "785 420", "+2.8 %")
    cols[1].metric("Emplois tech", "142 000", "+19 %")
    cols[2].metric("Startups", "1 620", "dont 14 licornes")
    cols[3].metric("Satisfaction", "86.4 %", "résidents 2025")

elif page == "Population":
    st.title("Population")
    df = load_data("POP_RECENSEMENT.csv")

    if not df.empty:
        st.subheader("Population totale par période")
        total = df[df["Âge"] == "Total"].groupby("Période")["Valeur"].sum().reset_index()
        fig = px.line(total, x="Période", y="Valeur", title="Évolution population")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Répartition par sexe (dernière période)")
        last = df["Période"].max()
        sex = df[(df["Période"] == last) & (df["Sexe"] != "Total")]
        fig_pie = px.pie(sex, values="Valeur", names="Sexe")
        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Extrait données")
        st.dataframe(df.head(10))
    else:
        st.warning("Données non disponibles")

elif page == "Emploi / Chômage":
    st.title("Emploi / Chômage")
    df = load_data("POP_CHOMAGE_DARES.csv")

    if not df.empty:
        st.dataframe(df.head(10))
        st.info("Graphiques et filtres à venir")
    else:
        st.warning("Données non disponibles")

elif page == "Économie":
    st.title("Économie")
    files = ["ECO_ENT_CREATION.csv", "ECO_ETAB_FLORES_5.csv", "ECO_ETAB_STOCKS.csv"]
    for f in files:
        df = load_data(f)
        if not df.empty:
            st.subheader(f.replace(".csv", ""))
            st.dataframe(df.head(8))

elif page == "Social / Ménages":
    st.title("Social / Ménages")
    files = ["POP_MENAGES.csv", "POP_FILOSOFI_MENAGE_MONO.csv", "POP_FILOSOFI_AGE.csv"]
    for f in files:
        df = load_data(f)
        if not df.empty:
            st.subheader(f.replace(".csv", ""))
            st.dataframe(df.head(8))

elif page == "Santé":
    st.title("Santé")
    st.info("Indicateurs santé à venir (données non encore intégrées)")

elif page == "Éducation":
    st.title("Éducation")
    st.info("Indicateurs éducation à venir (données non encore intégrées)")

elif page == "Sports":
    st.title("Sports")
    st.info("Indicateurs sports à venir (données non encore intégrées)")

elif page == "Finance (restreint)":
    st.title("Finance – Accès restreint")
    password = st.text_input("Mot de passe", type="password")
    if password == "paris-saclay2026":  # ← change ce mot de passe !!!
        st.success("Accès autorisé")
        st.info("Données financières sensibles – à venir")
    else:
        st.error("Mot de passe incorrect")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#64748b; margin:100px 0 40px;">
    © Communauté Paris-Saclay | Données février 2026 | App Streamlit
</div>
""", unsafe_allow_html=True)
