# app.py - Observatoire Territorial Paris-Saclay - Ultra Waouh + KPI réels Économie
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

# ─── Charte Paris-Saclay + lisibilité max ───────────────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
BLACK = "#000000"
DARK_GRAY = "#1A1F2E"
LIGHT_GRAY = "#E0E0E0"
WHITE = "#FFFFFF"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"

# ─── CSS ultra waouh ────────────────────────────────────────────────────────────
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {{
        --bg: {DARK_GRAY};
        --bg-card: rgba(26, 31, 46, 0.85);
        --text: {WHITE};
        --yellow: {YELLOW};
        --violet: {VIOLET};
        --accent-yellow: {ACCENT_YELLOW};
        --accent-violet: {ACCENT_VIOLET};
        --glow-yellow: 0 0 35px rgba(253, 209, 0, 0.7);
        --glow-violet: 0 0 35px rgba(106, 27, 154, 0.7);
    }}

    body, .stApp {{
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}

    .hero {{
        height: 80vh;
        background: linear-gradient(135deg, rgba(106,27,154,0.75), rgba(0,0,0,0.9)),
                    url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.8);
    }}

    .hero h1 {{
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(90deg, var(--yellow), var(--accent-violet), var(--yellow));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200%;
        animation: gradientFlow 10s ease infinite;
        text-shadow: var(--glow-yellow);
    }}

    @keyframes gradientFlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 40px;
        margin: 80px 0;
    }}

    .kpi-hex {{
        background: var(--bg-card);
        backdrop-filter: blur(24px);
        border: 3px solid var(--violet);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        padding: 52px 36px;
        text-align: center;
        transition: all 0.6s;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        position: relative;
        overflow: hidden;
    }}

    .kpi-hex:hover {{
        transform: scale(1.14) rotate(3deg);
        border-color: var(--yellow);
        box-shadow: 0 50px 140px rgba(253, 209, 0, 0.6),
                    0 50px 140px rgba(106, 27, 154, 0.6);
    }}

    .kpi-number {{
        font-size: 5rem;
        font-weight: 900;
        color: var(--accent-yellow);
        margin: 20px 0 16px;
        text-shadow: var(--glow-yellow);
    }}

    .sidebar .sidebar-content {{
        background: rgba(10, 14, 23, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid var(--violet);
    }}

    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ─── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <h1>Observatoire Territorial</h1>
        <p style="font-size:1.9rem; margin:2.5rem 0; color:#E0E0E0;">
            Agglomération Paris-Saclay — Indicateurs stratégiques en temps réel
        </p>
    </div>
</div>
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

# ─── Chargement données GitHub raw ──────────────────────────────────────────────
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

    # KPI hexagonales waouh (fictifs + réels quand possible)
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

    kpis = [
        ("Population", "785 420", "+2.8 %", YELLOW),
        ("Emplois tech", "142 000", "+19 %", VIOLET),
        ("Startups", "1 620", "14 licornes", YELLOW),
        ("Satisfaction", "86.4 %", "2025", VIOLET),
        ("Invest. R&D", "3.8 Md€", "cumulé", YELLOW)
    ]

    cols = st.columns(5)
    for col, (label, value, delta, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-hex" style="border-color:{color};">
                <h3 style="color:{color};">{label}</h3>
                <div class="kpi-number" style="color:{color};">{value}</div>
                <p style="color:#E0E0E0;">{delta}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─── Population ─────────────────────────────────────────────────────────────────
elif page == "Population":
    st.title("Population")
    df = load_data("POP_RECENSEMENT.csv")

    if not df.empty:
        df = df.rename(columns=lambda x: x.strip())

        # KPI Population
        total_latest = df[(df["Âge"] == "Total") & (df["Sexe"] == "Total")]["Valeur"].iloc[-1]
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Population totale</h3>
                <div class="kpi-number" style="color:{YELLOW};">{int(total_latest):,}</div>
                <p style="color:#E0E0E0;">Dernière période</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Courbe évolution
        total = df[df["Âge"] == "Total"].groupby("Période")["Valeur"].sum().reset_index()
        fig_line = px.line(total, x="Période", y="Valeur",
                           title="Évolution population totale",
                           color_discrete_sequence=[YELLOW])
        fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color=WHITE)
        st.plotly_chart(fig_line, use_container_width=True)

        # Camembert âges
        last = df["Période"].max()
        age_df = df[(df["Période"] == last) & (df["Âge"] != "Total") & (df["Sexe"] == "Total")]
        colors = [VIOLET, YELLOW, "#9F7AEA", "#D6BCFA", "#FBBF24", "#F87171"]
        fig_pie = px.pie(age_df, values="Valeur", names="Âge",
                         color_discrete_sequence=colors,
                         title=f"Répartition par âge en {last}")
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color=WHITE)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.dataframe(df.head(12).style.background_gradient(cmap='YlOrBr_r'))

    else:
        st.warning("Données Population non disponibles")

# ─── Emploi / Chômage ──────────────────────────────────────────────────────────
elif page == "Emploi / Chômage":
    st.title("Emploi / Chômage")
    df = load_data("POP_CHOMAGE_DARES.csv")

    if not df.empty:
        # KPI exemple (à affiner avec tes données)
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Taux chômage</h3>
                <div class="kpi-number" style="color:{YELLOW};">8.2 %</div>
                <p style="color:#E0E0E0;">(estimation 2025)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(df.head(10).style.background_gradient(cmap='YlOrBr_r'))
    else:
        st.warning("Données Emploi/Chômage non disponibles")

# ─── Économie ───────────────────────────────────────────────────────────────────
elif page == "Économie":
    st.title("Économie")

    # Chargement des 3 fichiers
    creation = load_data("ECO_ENT_CREATION.csv")
    flores = load_data("ECO_ETAB_FLORES_5.csv")
    stocks = load_data("ECO_ETAB_STOCKS.csv")

    # KPI Économie - créations récentes
    if not creation.empty:
        last_year = creation["Période"].max()
        nb_creations = creation[creation["Période"] == last_year]["Valeur"].sum()
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Créations d'entreprises</h3>
                <div class="kpi-number" style="color:{YELLOW};">{int(nb_creations):,}</div>
                <p style="color:#E0E0E0;">en {last_year}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stocks d'établissements
    if not stocks.empty:
        total_stocks = stocks[stocks["Activité économique"] == "Total"]["Valeur"].iloc[-1]
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{VIOLET};">
                <h3 style="color:{VIOLET};">Établissements actifs</h3>
                <div class="kpi-number" style="color:{VIOLET};">{int(total_stocks):,}</div>
                <p style="color:#E0E0E0;">Dernière période</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tableau extraits
    if not creation.empty:
        st.subheader("Créations d'entreprises (extrait)")
        st.dataframe(creation.head(10).style.background_gradient(cmap='YlOrBr_r'))

    if not stocks.empty:
        st.subheader("Stocks d'établissements (extrait)")
        st.dataframe(stocks.head(10).style.background_gradient(cmap='YlOrBr_r'))

# ─── Social / Ménages ───────────────────────────────────────────────────────────
elif page == "Social / Ménages":
    st.title("Social / Ménages")
    files = ["POP_MENAGES.csv", "POP_FILOSOFI_MENAGE_MONO.csv", "POP_FILOSOFI_AGE.csv"]
    for f in files:
        df = load_data(f)
        if not df.empty:
            st.subheader(f.replace(".csv", ""))
            st.dataframe(df.head(8).style.background_gradient(cmap='YlOrBr_r'))

# ─── Santé, Éducation, Sports ───────────────────────────────────────────────────
elif page in ["Santé", "Éducation", "Sports"]:
    st.title(page)
    st.markdown(f"""
    <div class='kpi-grid'>
        <div class="kpi-hex" style="border-color:{VIOLET};">
            <h3 style="color:{VIOLET};">Indicateur clé</h3>
            <div class="kpi-number" style="color:{VIOLET};">En cours</div>
            <p style="color:#E0E0E0;">Données à intégrer</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info(f"Page {page} en construction – indicateurs à venir")

# ─── Finance restreinte ─────────────────────────────────────────────────────────
elif page == "Finance (restreint)":
    st.title("Finance – Accès sécurisé")
    pwd = st.text_input("Mot de passe", type="password")
    if pwd == "saclay2026":  # À CHANGER !!!
        st.success("Accès autorisé")
        st.markdown("""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Budget</h3>
                <div class="kpi-number" style="color:{YELLOW};">En cours</div>
                <p style="color:#E0E0E0;">Données sensibles</p>
            </div>
        </div>
        """.format(YELLOW=YELLOW), unsafe_allow_html=True)
        st.info("Données financières à intégrer prochainement")
    else:
        st.error("Accès refusé")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:#888; margin:120px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Déployé via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
