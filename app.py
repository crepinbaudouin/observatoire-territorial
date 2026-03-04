# app.py - Observatoire Territorial Paris-Saclay - Fond d'écran sur toutes les pages
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

# ─── Fond d'écran sur TOUTES les pages ─────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url({fond_url});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Légère superposition sombre pour améliorer la lisibilité */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(26, 31, 46, 0.75);  /* Gris foncé semi-transparent */
            z-index: -1;
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Couleurs charte Paris-Saclay ──────────────────────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
BLACK = "#000000"
DARK_GRAY = "#1A1F2E"
LIGHT_GRAY = "#E0E0E0"
WHITE = "#FFFFFF"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"

# ─── CSS waouh (adapté au fond) ─────────────────────────────────────────────────
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    .hero {{
        height: 80vh;
        background: linear-gradient(135deg, rgba(106,27,154,0.65), rgba(0,0,0,0.8)),
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
        animation: gradientFlow 10s ease infinite;
        text-shadow: 0 0 35px rgba(253, 209, 0, 0.9);
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
        background: rgba(26, 31, 46, 0.92);
        backdrop-filter: blur(24px);
        border: 3px solid var(--violet);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        padding: 52px 36px;
        text-align: center;
        transition: all 0.6s;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }}

    .kpi-hex:hover {{
        transform: scale(1.14) rotate(3deg);
        border-color: var(--yellow);
        box-shadow: 0 50px 140px rgba(253, 209, 0, 0.7);
    }}

    .kpi-number {{
        font-size: 5rem;
        font-weight: 900;
        color: var(--accent-yellow);
        margin: 20px 0 16px;
        text-shadow: 0 0 35px rgba(253, 209, 0, 0.9);
    }}

    .sidebar .sidebar-content {{
        background: rgba(10, 14, 23, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid var(--violet);
    }}

    footer {{visibility: hidden;}}
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

    # 5 KPI hexagonales waouh
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

    kpis = [
        ("Population totale", "785 420", "+2.8 %", YELLOW),
        ("Emplois tech & R&D", "142 000", "+19 %", VIOLET),
        ("Startups actives", "1 620", "14 licornes", YELLOW),
        ("Satisfaction résidents", "86.4 %", "2025", VIOLET),
        ("Investissements R&D", "3.8 Md€", "cumulé", YELLOW)
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

    recensement = load_data("POP_RECENSEMENT.csv")
    naissances = load_data("POP_NAISSANCES.csv")
    deces = load_data("POP_DECES.csv")
    migration = load_data("POP_MIGRATION.csv")

    if not recensement.empty:
        recensement = recensement.rename(columns=lambda x: x.strip())

        # Filtres interactifs
        st.subheader("Filtres")
        col1, col2 = st.columns(2)
        with col1:
            annees = sorted(recensement["Période"].unique())
            annee_selectionnee = st.selectbox("Année", annees, index=len(annees)-1)

        with col2:
            communes = ["Toutes"] + sorted(recensement["Géographie"].unique().tolist())
            commune_selectionnee = st.selectbox("Commune / Niveau", communes)

        # Filtrage
        df_filtre = recensement[recensement["Période"] == annee_selectionnee]
        if commune_selectionnee != "Toutes":
            df_filtre = df_filtre[df_filtre["Géographie"] == commune_selectionnee]

        # 5 KPI Population animés
        st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

        total_latest = df_filtre[(df_filtre["Âge"] == "Total") & (df_filtre["Sexe"] == "Total")]["Valeur"].sum()
        young = df_filtre[(df_filtre["Âge"].str.contains("Moins de 15|Moins de 20", na=False))]["Valeur"].sum()
        elderly = df_filtre[(df_filtre["Âge"].str.contains("65 ans|65 ou plus", na=False))]["Valeur"].sum()
        solde_naturel = naissances[naissances["Période"] == annee_selectionnee]["Valeur"].sum() - deces[deces["Période"] == annee_selectionnee]["Valeur"].sum() if not naissances.empty and not deces.empty else 0
        solde_mig = migration[migration["Période"] == annee_selectionnee]["Valeur"].sum() if not migration.empty else "N/A"

        kpis_pop = [
            ("Population totale", int(total_latest), f"{annee_selectionnee}", YELLOW),
            ("Moins de 20 ans", int(young), "jeunes", VIOLET),
            ("65 ans et plus", int(elderly), "seniors", YELLOW),
            ("Solde naturel", int(solde_naturel), "naissances - décès", VIOLET),
            ("Solde migratoire", solde_mig, "cumulé", YELLOW)
        ]

        cols = st.columns(5)
        for col, (label, value, delta, color) in zip(cols, kpis_pop):
            with col:
                animated_counter(label, value, delta, color)

        st.markdown("</div>", unsafe_allow_html=True)

        # Graphiques filtrés
        total = df_filtre[df_filtre["Âge"] == "Total"].groupby("Période")["Valeur"].sum().reset_index()
        fig_line = px.line(total, x="Période", y="Valeur", title=f"Évolution population - {commune_selectionnee}", color_discrete_sequence=[YELLOW])
        fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color=WHITE)
        st.plotly_chart(fig_line, use_container_width=True)

        age_df = df_filtre[(df_filtre["Âge"] != "Total") & (df_filtre["Sexe"] == "Total")]
        colors = [VIOLET, YELLOW, "#9F7AEA", "#D6BCFA", "#FBBF24", "#F87171"]
        fig_pie = px.pie(age_df, values="Valeur", names="Âge", color_discrete_sequence=colors, title=f"Répartition par âge en {annee_selectionnee}")
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color=WHITE)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.dataframe(df_filtre.head(12).style.background_gradient(cmap='YlOrBr_r'))

    else:
        st.warning("Données Population non disponibles")

# ─── Fonction compteur animé ────────────────────────────────────────────────────
def animated_counter(label, final_value, delta="", color=YELLOW, duration=2.0):
    placeholder = st.empty()
    start = time.time()
    value = 0
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

# ─── Autres pages (exemples avec 4 KPI) ─────────────────────────────────────────
elif page == "Économie":
    st.title("Économie")
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

    kpis_eco = [
        ("Créations entreprises", 1620, "2024", YELLOW),
        ("Établissements actifs", 27258, "2023", VIOLET),
        ("Invest. innovation", 2800000000, "2025", YELLOW),
        ("Chiffre d'affaires estimé", 12500000000, "+4.1 %", VIOLET)
    ]

    cols = st.columns(4)
    for col, (label, value, delta, color) in zip(cols, kpis_eco):
        with col:
            animated_counter(label, value, delta, color)

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Social / Ménages":
    st.title("Social / Ménages")
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

    kpis_soc = [
        ("Ménages monoparentaux", 18.7, "% 2021", YELLOW),
        ("Taille moyenne ménage", 2.4, "pers.", VIOLET),
        ("Revenu médian", 27650, "€ 2021", YELLOW),
        ("Taux pauvreté global", 10.1, "% 2021", VIOLET)
    ]

    cols = st.columns(4)
    for col, (label, value, delta, color) in zip(cols, kpis_soc):
        with col:
            animated_counter(label, value, delta, color)

    st.markdown("</div>", unsafe_allow_html=True)

elif page in ["Santé", "Éducation", "Sports"]:
    st.title(page)
    st.markdown(f"""
    <div class='kpi-grid'>
        <div class="kpi-hex" style="border-color:{YELLOW};">
            <h3 style="color:{YELLOW};">Indicateur 1</h3>
            <div class="kpi-number" style="color:{YELLOW};">En cours</div>
            <p style="color:#E0E0E0;">Données à venir</p>
        </div>
        <div class="kpi-hex" style="border-color:{VIOLET};">
            <h3 style="color:{VIOLET};">Indicateur 2</h3>
            <div class="kpi-number" style="color:{VIOLET};">En cours</div>
            <p style="color:#E0E0E0;">Données à venir</p>
        </div>
        <div class="kpi-hex" style="border-color:{YELLOW};">
            <h3 style="color:{YELLOW};">Indicateur 3</h3>
            <div class="kpi-number" style="color:{YELLOW};">En cours</div>
            <p style="color:#E0E0E0;">Données à venir</p>
        </div>
        <div class="kpi-hex" style="border-color:{VIOLET};">
            <h3 style="color:{VIOLET};">Indicateur 4</h3>
            <div class="kpi-number" style="color:{VIOLET};">En cours</div>
            <p style="color:#E0E0E0;">Données à venir</p>
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
        st.markdown(f"""
        <div class='kpi-grid'>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Budget 2026</h3>
                <div class="kpi-number" style="color:{YELLOW};">En cours</div>
                <p style="color:#E0E0E0;">Données sensibles</p>
            </div>
            <div class="kpi-hex" style="border-color:{VIOLET};">
                <h3 style="color:{VIOLET};">Investissement</h3>
                <div class="kpi-number" style="color:{VIOLET};">En cours</div>
                <p style="color:#E0E0E0;">Données sensibles</p>
            </div>
            <div class="kpi-hex" style="border-color:{YELLOW};">
                <h3 style="color:{YELLOW};">Dette</h3>
                <div class="kpi-number" style="color:{YELLOW};">En cours</div>
                <p style="color:#E0E0E0;">Données sensibles</p>
            </div>
            <div class="kpi-hex" style="border-color:{VIOLET};">
                <h3 style="color:{VIOLET};">Résultat net</h3>
                <div class="kpi-number" style="color:{VIOLET};">En cours</div>
                <p style="color:#E0E0E0;">Données sensibles</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.info("Données financières sensibles – à intégrer prochainement")
    else:
        st.error("Accès refusé")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:#888; margin:120px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Déployé via Streamlit Cloud
</div>
""", unsafe_allow_html=True)
