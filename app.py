# app.py - Observatoire Territorial Paris-Saclay - Responsive Mobile + KPI animés
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Fond d'écran ───────────────────────────────────────────────────────────────
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

        /* Responsive mobile */
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: 1fr !important;
                gap: 20px !important;
                margin: 40px 0 !important;
            }}
            .kpi-hex {{
                padding: 30px 20px !important;
            }}
            .kpi-number {{
                font-size: 3.5rem !important;
            }}
            h1, h2, h3 {{
                font-size: 2rem !important;
                text-align: center !important;
            }}
            .sidebar .sidebar-content {{
                padding: 10px !important;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                flex-direction: column !important;
                gap: 10px !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                width: 100% !important;
                text-align: center !important;
            }}
        }}

        /* Tablette et plus grand */
        @media (min-width: 769px) {{
            .kpi-grid {{
                grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            }}
        }}

        .kpi-grid {{
            display: grid;
            gap: 40px;
            margin: 80px 0;
        }}

        .kpi-hex {{
            background: rgba(26, 31, 46, 0.92);
            backdrop-filter: blur(24px);
            border: 3px solid #6A1B9A;
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            padding: 52px 36px;
            text-align: center;
            transition: all 0.6s;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        }}

        .kpi-hex:hover {{
            transform: scale(1.14) rotate(3deg);
            border-color: #FDD100;
            box-shadow: 0 50px 140px rgba(253, 209, 0, 0.7);
        }}

        .kpi-number {{
            font-size: 5rem;
            font-weight: 900;
            color: #FFE066;
            margin: 20px 0 16px;
            text-shadow: 0 0 35px rgba(253, 209, 0, 0.9);
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
def animated_counter(label, final_value, delta="", color="#FDD100", duration=2.0):
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

# ─── Chargement données (exemple) ───────────────────────────────────────────────
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        return pd.read_csv(url, sep=";", decimal=",", low_memory=False)
    except:
        return pd.DataFrame()

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
        recensement = recensement.rename(columns=lambda x: x.strip())

        # Filtres
        st.subheader("Filtres")
        col1, col2 = st.columns(2)
        with col1:
            annees = sorted(recensement["Période"].unique())
            annee_selectionnee = st.selectbox("Année", annees, index=len(annees)-1)

        with col2:
            communes = ["Toutes"] + sorted(recensement["Géographie"].unique().tolist())
            commune_selectionnee = st.selectbox("Commune / Niveau", communes)

        df_filtre = recensement[recensement["Période"] == annee_selectionnee]
        if commune_selectionnee != "Toutes":
            df_filtre = df_filtre[df_filtre["Géographie"] == commune_selectionnee]

        # KPI animés
        st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

        total_latest = df_filtre[(df_filtre["Âge"] == "Total") & (df_filtre["Sexe"] == "Total")]["Valeur"].sum()
        young = df_filtre[(df_filtre["Âge"].str.contains("Moins de 15|Moins de 20", na=False))]["Valeur"].sum()
        elderly = df_filtre[(df_filtre["Âge"].str.contains("65 ans|65 ou plus", na=False))]["Valeur"].sum()

        kpis_pop = [
            ("Population totale", int(total_latest), f"{annee_selectionnee}", YELLOW),
            ("Moins de 20 ans", int(young), "jeunes", VIOLET),
            ("65 ans et plus", int(elderly), "seniors", YELLOW),
            ("Croissance récente", 28, "+2.8 %", VIOLET)
        ]

        cols = st.columns(4)
        for col, (label, value, delta, color) in zip(cols, kpis_pop):
            with col:
                animated_counter(label, value, delta, color)

        st.markdown("</div>", unsafe_allow_html=True)

# ─── Autres pages (exemple avec 4 KPI animés) ───────────────────────────────────
else:
    st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

    kpis_placeholder = [
        ("Indicateur 1", 1234, "2025", YELLOW),
        ("Indicateur 2", 5678, "+5 %", VIOLET),
        ("Indicateur 3", 91011, "stable", YELLOW),
        ("Indicateur 4", 1213, "en cours", VIOLET)
    ]

    cols = st.columns(4)
    for col, (label, value, delta, color) in zip(cols, kpis_placeholder):
        with col:
            animated_counter(label, value, delta, color)

    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Page {page} en construction – indicateurs à venir")

# Footer
st.markdown(f"""
<div style="text-align:center; color:#888; margin:120px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Déployé via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
