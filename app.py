# app.py - Observatoire Territorial Paris-Saclay - Ultra Waouh + Lisibilité Charte
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ─── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Couleurs charte Paris-Saclay + haute lisibilité ────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
BLACK = "#000000"
DARK_GRAY = "#1A1F2E"
LIGHT_GRAY = "#E0E0E0"
WHITE = "#FFFFFF"
ACCENT_YELLOW = "#FFE066"  # jaune plus clair pour texte sur fond sombre
ACCENT_VIOLET = "#9F7AEA"  # violet clair pour contraste

# ─── CSS ultra waouh + lisibilité renforcée ─────────────────────────────────────
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
        animation: heroPulse 10s infinite alternate;
    }}

    @keyframes heroPulse {{
        0% {{ opacity: 0.93; }}
        100% {{ opacity: 1; }}
    }}

    .hero h1 {{
        font-size: 6rem;
        font-weight: 900;
        margin: 0;
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

    .hero-subtitle {{
        font-size: 1.9rem;
        margin: 2.5rem 0 4rem;
        color: var(--light-gray);
        max-width: 1000px;
    }}

    .btn-glow {{
        background: linear-gradient(45deg, var(--yellow), var(--violet));
        color: var(--black);
        padding: 18px 56px;
        font-size: 1.5rem;
        font-weight: 800;
        border: none;
        border-radius: 60px;
        cursor: pointer;
        transition: all 0.45s;
        box-shadow: var(--glow-yellow), var(--glow-violet);
        margin: 0 24px;
    }}

    .btn-glow:hover {{
        transform: translateY(-8px) scale(1.1);
        box-shadow: 0 0 90px rgba(253, 209, 0, 1),
                    0 0 90px rgba(106, 27, 154, 0.9);
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

# ─── Hero ultra waouh ───────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <h1>Observatoire Territorial</h1>
        <p class="hero-subtitle">
            Agglomération Paris-Saclay — Indicateurs stratégiques en temps réel
        </p>
        <div>
            <button class="btn-glow">Explorer les indicateurs</button>
            <button class="btn-glow" style="background:transparent; border:3px solid var(--yellow); color:var(--yellow);">
                Finance sécurisée
            </button>
        </div>
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

# ─── Accueil ────────────────────────────────────────────────────────────────────
if page == "Accueil":
    st.title("Observatoire Territorial Paris-Saclay")

    # KPI hexagonales ultra waouh
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

    st.markdown("""
    <div style="text-align:center; margin:80px 0;">
        <h2 style="color:var(--yellow);">Bienvenue dans l'Observatoire</h2>
        <p style="font-size:1.4rem; color:#E0E0E0;">
            Sélectionnez une thématique dans la barre latérale pour explorer les indicateurs clés.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Population ─────────────────────────────────────────────────────────────────
elif page == "Population":
    st.title("Population")
    df = pd.read_csv("https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/POP_RECENSEMENT.csv", sep=";", decimal=",")

    if not df.empty:
        df = df.rename(columns=lambda x: x.strip())

        # Indicateur 1 : Évolution population totale
        st.subheader("Évolution de la population totale")
        total = df[df["Âge"] == "Total"].groupby("Période")["Valeur"].sum().reset_index()
        fig_line = px.line(total, x="Période", y="Valeur",
                           title="Évolution population totale",
                           color_discrete_sequence=[YELLOW])
        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=WHITE,
            title_font_color=YELLOW
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Indicateur 2 : Répartition par âge (dernière période) - couleurs lisibles
        st.subheader("Répartition par âge – Dernière période")
        last = df["Période"].max()
        age_df = df[(df["Période"] == last) & (df["Âge"] != "Total") & (df["Sexe"] == "Total")]
        colors = [VIOLET, YELLOW, "#9F7AEA", "#D6BCFA", "#FBBF24", "#F87171"]  # palette lisible
        fig_pie = px.pie(age_df, values="Valeur", names="Âge",
                         color_discrete_sequence=colors,
                         title=f"Répartition par âge en {last}")
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=WHITE,
            legend_title_font_color=WHITE,
            legend_font_color=WHITE
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Tableau extrait
        st.subheader("Données brutes (extrait)")
        st.dataframe(df.head(12).style.background_gradient(cmap='YlOrBr'))

    else:
        st.warning("Données POP_RECENSEMENT.csv non disponibles")

# ─── Autres pages (placeholders enrichis) ───────────────────────────────────────
elif page == "Emploi / Chômage":
    st.title("Emploi / Chômage")
    df = pd.read_csv("https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/POP_CHOMAGE_DARES.csv", sep=";", decimal=",")
    if not df.empty:
        st.subheader("Extrait des données")
        st.dataframe(df.head(10).style.background_gradient(cmap='YlOrBr'))
    else:
        st.warning("Données non disponibles")

elif page == "Économie":
    st.title("Économie")
    files = ["ECO_ENT_CREATION.csv", "ECO_ETAB_FLORES_5.csv", "ECO_ETAB_STOCKS.csv"]
    for f in files:
        df = pd.read_csv(f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{f}", sep=";", decimal=",")
        if not df.empty:
            st.subheader(f.replace(".csv", ""))
            st.dataframe(df.head(8).style.background_gradient(cmap='YlOrBr'))

elif page == "Social / Ménages":
    st.title("Social / Ménages")
    files = ["POP_MENAGES.csv", "POP_FILOSOFI_MENAGE_MONO.csv", "POP_FILOSOFI_AGE.csv"]
    for f in files:
        df = pd.read_csv(f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{f}", sep=";", decimal=",")
        if not df.empty:
            st.subheader(f.replace(".csv", ""))
            st.dataframe(df.head(8).style.background_gradient(cmap='YlOrBr'))

elif page in ["Santé", "Éducation", "Sports"]:
    st.title(page)
    st.info(f"Indicateurs {page.lower()} à venir – données non encore intégrées")

elif page == "Finance (restreint)":
    st.title("Finance – Accès sécurisé")
    pwd = st.text_input("Mot de passe", type="password")
    if pwd == "saclay2026":  # À CHANGER !!!
        st.success("Accès autorisé")
        st.info("Données financières sensibles – à intégrer prochainement")
    else:
        st.error("Accès refusé")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:#888; margin:120px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Déployé via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
