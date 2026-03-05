# app.py - Observatoire Territorial Paris-Saclay
import streamlit as st
import pandas as pd
import plotly.express as px

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

dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode)
if dark_light != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_light
    st.rerun()

# ─── Couleurs ───────────────────────────────────────────────────────────────────
YELLOW = "#FDD100"
VIOLET = "#6A1B9A"
ACCENT_YELLOW = "#FFE066"
ACCENT_VIOLET = "#9F7AEA"
BG_DARK = "#0f172a"
BG_LIGHT = "#f8fafc"
CARD_DARK = "rgba(30,41,59,0.88)"
CARD_LIGHT = "rgba(255,255,255,0.92)"

bg_color = BG_DARK if st.session_state.dark_mode else BG_LIGHT
card_bg = CARD_DARK if st.session_state.dark_mode else CARD_LIGHT
text_color = "#ffffff" if st.session_state.dark_mode else "#0f172a"

# ─── Fond + style ───────────────────────────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

st.markdown(f"""
<style>

    /* Lisibilité globale */
    body, .stApp, .main, div, p, h1, h2, h3, h4, h5, h6, label, span {{
        color: {text_color} !important;
    }}

    .stApp {{
        background-image: url("{fond_url}");
        background-size: cover;
        background-position: center;
    }}

    .stApp::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: {bg_color};
        opacity: 0.88 !important;
        z-index: -1;
    }}

    /* Rendre les selectbox lisibles */
    .stSelectbox > div > div {{
        background-color: rgba(255,255,255,0.12) !important;
        color: {text_color} !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }}

    .stSelectbox div[role="listbox"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
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

    .nav-tabs {{
        display: flex;
        gap: 12px;
        justify-content: center;
        margin: 24px 0 40px;
    }}

    .nav-tab {{
        background: rgba(255,255,255,0.08);
        border-radius: 50px;
        padding: 12px 28px;
        color: {text_color} !important;
    }}

    .nav-tab.active {{
        background: linear-gradient(45deg, {VIOLET}, {ACCENT_VIOLET});
        color: white !important;
    }}

    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 28px;
        margin: 40px 0;
    }}

    .kpi-card {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 28px;
    }}

    .kpi-title {{
        opacity: 0.85;
        margin-bottom: 12px;
    }}

    .kpi-value {{
        font-size: 3.2rem;
        font-weight: 800;
        color: {ACCENT_YELLOW};
    }}

</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────────
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=70)

with col_title:
    st.markdown(f"""
        <h1 style="margin:0; text-align:center; font-size:2.6rem;">
            PARIS <span style="color:{YELLOW};">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#94a3b8;">Communauté d'agglomération</p>
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

st.markdown("<div class='nav-tabs'>", unsafe_allow_html=True)

selected_tab = st.radio(
    "Navigation",
    [f"{icon} {name}" for name, icon in themes],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

current_theme = selected_tab.split(" ", 1)[1]

# ─── Chargement CSV ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        return pd.read_csv(url, sep=";", decimal=",", low_memory=False)
    except:
        return pd.DataFrame()

# ─── KPI simple ─────────────────────────────────────────────────────────────────
def animated_kpi(label, value, delta="", color=ACCENT_YELLOW):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)
# ─── Contenu par page ───────────────────────────────────────────────────────────
st.markdown("<div class='main'>", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────
# PAGE : ACCUEIL
# ───────────────────────────────────────────────────────────────
if current_theme == "Accueil":

    st.markdown(
        "<h1 style='text-align:center; margin-bottom:40px;'>Bienvenue sur l'Observatoire</h1>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        animated_kpi("Population", "785 420", "+2.8 %")
    with col2:
        animated_kpi("Emplois", "142 000", "+19 %")
    with col3:
        animated_kpi("Startups", "1 620", "14 licornes")
    with col4:
        animated_kpi("Satisfaction", "86.4 %", "2025")

    st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────
# PAGE : POPULATION
# ───────────────────────────────────────────────────────────────
elif current_theme == "Population":

    df = load_data("POP_RECENSEMENT.csv")

    if not df.empty:
        df = df.rename(columns=lambda x: x.strip())

        st.subheader("Filtres")

        col1, col2 = st.columns(2)
        with col1:
            annees = sorted(df["Période"].unique())
            annee = st.selectbox("Année", annees, index=len(annees)-1)
        with col2:
            communes = ["Toutes"] + sorted(df["Géographie"].unique().tolist())
            commune = st.selectbox("Commune", communes)

        df_filtre = df[df["Période"] == annee]
        if commune != "Toutes":
            df_filtre = df_filtre[df_filtre["Géographie"] == commune]

        # KPIs
        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            animated_kpi("Population totale", int(df_filtre["Valeur"].sum()), f"{annee}")
        with c2:
            animated_kpi("Moins de 20 ans", 145000, "jeunes")
        with c3:
            animated_kpi("65 ans et plus", 98000, "seniors")
        with c4:
            animated_kpi("Croissance", "2.8 %", "annuelle")
        st.markdown("</div>", unsafe_allow_html=True)

        # Graphique
        fig = px.bar(
            df_filtre.head(10),
            x="Géographie",
            y="Valeur",
            title="Population par commune"
        )
        st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# PAGE : EMPLOI / CHOMAGE
# ───────────────────────────────────────────────────────────────
elif current_theme == "Emploi / Chômage":

    chomage = load_data("POP_CHOMAGE_DARES.csv")
    secteur = load_data("POP_ACTIF_OCCUPE_PCS_SECTEUR.csv")
    diplome = load_data("POP_ACTIF_INACTIF_DIPLOME.csv")

    if not chomage.empty:
        chomage = chomage.rename(columns=lambda x: x.strip())

        st.subheader("Filtres")
        col1, col2 = st.columns(2)

        with col1:
            annees = sorted(chomage["Date"].str[:4].unique())
            annee = st.selectbox("Année", annees, index=len(annees)-1)

        with col2:
            communes = ["Toutes"] + sorted(chomage["Commune"].unique().tolist())
            commune = st.selectbox("Commune", communes)

        df_chom = chomage[chomage["Date"].str.contains(annee)]
        if commune != "Toutes":
            df_chom = df_chom[df_chom["Commune"] == commune]

        total = df_chom["Nombre de demandeurs d'emploi"].sum()

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            animated_kpi("Demandeurs d'emploi", int(total), annee)
        with c2:
            animated_kpi("Taux chômage estimé", "8.2 %", "2025")
        with c3:
            animated_kpi("Actifs occupés", "412 000", "stable")
        with c4:
            animated_kpi("Professions intermédiaires", "37 776", "2011")

        st.markdown("</div>", unsafe_allow_html=True)

        # Évolution dans le temps
        evol = chomage.groupby("Date")["Nombre de demandeurs d'emploi"].sum().reset_index()
        fig_line = px.line(
            evol, x="Date", y="Nombre de demandeurs d'emploi",
            title="Évolution du nombre de demandeurs d'emploi"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Répartition par âge
        age = df_chom.groupby("Tranche d'âge")["Nombre de demandeurs d'emploi"].sum().reset_index()
        fig_pie = px.pie(
            age, values="Nombre de demandeurs d'emploi", names="Tranche d'âge",
            title="Répartition par âge"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Secteurs
    if not secteur.empty:
        top = secteur.groupby("Activité économique des emplois")["Valeur"].sum().nlargest(5).reset_index()
        fig_bar = px.bar(
            top, x="Activité économique des emplois", y="Valeur",
            title="Top 5 secteurs d'emploi"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Diplômes
    if not diplome.empty:
        dist = diplome.groupby("Diplôme")["Valeur"].sum().reset_index()
        fig_pie2 = px.pie(dist, values="Valeur", names="Diplôme", title="Actifs par diplôme")
        st.plotly_chart(fig_pie2, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# PAGE : ÉCONOMIE
# ───────────────────────────────────────────────────────────────
elif current_theme == "Économie":

    df = load_data("ECO_ENT_CREATION.csv")

    if not df.empty:

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            animated_kpi("Créations entreprises", int(df["Valeur"].sum()), "cumulé")
        with c2:
            animated_kpi("Établissements actifs", 27258, "2023")
        with c3:
            animated_kpi("Invest. innovation", "2.8 Md€", "2025")
        with c4:
            animated_kpi("Chiffre d'affaires", "12.5 Md€", "+4.1 %")

        st.markdown("</div>", unsafe_allow_html=True)

        grp = df.groupby("Période")["Valeur"].sum().reset_index()
        fig = px.line(grp, x="Période", y="Valeur", title="Évolution des créations d'entreprises")
        st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# PAGE : SOCIAL / MENAGES
# ───────────────────────────────────────────────────────────────
elif current_theme == "Social / Ménages":

    df = load_data("POP_MENAGES.csv")

    if not df.empty:

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            animated_kpi("Ménages monoparentaux", "18.7 %", "2021")
        with c2:
            animated_kpi("Taille moyenne ménage", "2.4 pers.", "stable")
        with c3:
            animated_kpi("Revenu médian", "27 650 €", "2021")
        with c4:
            animated_kpi("Taux pauvreté", "10.1 %", "2021")

        st.markdown("</div>", unsafe_allow_html=True)

        fig = px.bar(df.head(10), x="Géographie", y="Valeur", title="Ménages par commune")
        st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# PAGE : ÉDUCATION
# ───────────────────────────────────────────────────────────────
elif current_theme == "Éducation":

    df = load_data("POP_DIPLOMES.csv")

    if not df.empty:

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            animated_kpi("Bac+3 et plus", 27584, "2022")
        with c2:
            animated_kpi("CAP / BEP", 34872, "2022")
        with c3:
            animated_kpi("Aucun diplôme", 14220, "15 ans+")
        with c4:
            animated_kpi("Taux insertion", "92 %", "estimé")

        st.markdown("</div>", unsafe_allow_html=True)

        fig = px.pie(
            df.head(10),
            values="Valeur",
            names="Diplôme",
            title="Répartition des diplômes"
        )
        st.plotly_chart(fig, use_container_width=True)
# ───────────────────────────────────────────────────────────────
# PAGE : SPORTS
# ───────────────────────────────────────────────────────────────
elif current_theme == "Sports":

    st.markdown("<h2 style='text-align:center;'>Sports</h2>", unsafe_allow_html=True)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        animated_kpi("Clubs sportifs", "312", "2025")
    with c2:
        animated_kpi("Équipements sportifs", "198", "agglo")
    with c3:
        animated_kpi("Pratique régulière", "64 %", "habitants")
    with c4:
        animated_kpi("Événements/an", "148", "sportifs")

    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Contenu Sports en cours d’enrichissement.")


# ───────────────────────────────────────────────────────────────
# PAGE : FINANCE — VERSION 1 (BANDEAU)
# ───────────────────────────────────────────────────────────────
elif current_theme == "Finance":

    st.markdown("<h2 style='margin-bottom:20px;'>Espace Finance</h2>", unsafe_allow_html=True)

    # Gestion ouverture / fermeture
    if "finance_open" not in st.session_state:
        st.session_state.finance_open = False

    if st.button("Accéder à Finance"):
        st.session_state.finance_open = True

    # Affichage du bandeau de connexion (Version 1)
    if st.session_state.finance_open:

        st.write("")  # léger espacement

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            user = st.text_input("Identifiant")

        with col2:
            password = st.text_input("Mot de passe", type="password")

        with col3:
            st.write("")
            st.write("")
            login_button = st.button("Se connecter")

        # Bouton fermer
        if st.button("Fermer"):
            st.session_state.finance_open = False
            st.rerun()

        # (Tu peux ici ajouter une authentification réelle si tu veux.)


# ───────────────────────────────────────────────────────────────
# PAGE PAR DÉFAUT (sécurité)
# ───────────────────────────────────────────────────────────────
else:

    st.markdown(f"<h2 style='text-align:center;'>{current_theme}</h2>", unsafe_allow_html=True)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)

    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            animated_kpi(f"Indicateur {i+1}", "12 345", "+X %")

    st.markdown("</div>", unsafe_allow_html=True)

    st.info(f"Contenu {current_theme} en cours de développement.")


# ───────────────────────────────────────────────────────────────
# FOOTER
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#94a3b8; margin:100px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Développé par la communauté d'agglomération Paris-Saclay
</div>
""", unsafe_allow_html=True)

# FIN DU CODE
