# app.py - Observatoire Territorial Paris-Saclay - Emploi/Chômage réel + toutes pages
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
CARD_DARK = "rgba(30, 41, 59, 0.88)"
CARD_LIGHT = "rgba(255, 255, 255, 0.92)"

bg_color = BG_DARK if st.session_state.dark_mode else BG_LIGHT
card_bg = CARD_DARK if st.session_state.dark_mode else CARD_LIGHT
text_color = "#ffffff" if st.session_state.dark_mode else "#0f172a"

# ─── Fond + style ───────────────────────────────────────────────────────────────
fond_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg"

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
    .logo-title h1 {{
        margin: 0;
        font-size: 2.4rem;
        background: linear-gradient(90deg, {YELLOW}, {ACCENT_VIOLET});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .nav-tabs {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        justify-content: center;
        margin: 24px 0 40px;
    }}
    .nav-tab {{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 50px;
        padding: 12px 28px;
        color: white;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .nav-tab:hover {{
        background: rgba(253,209,0,0.15);
        transform: translateY(-2px);
    }}
    .nav-tab.active {{
        background: linear-gradient(45deg, {VIOLET}, {ACCENT_VIOLET});
        box-shadow: 0 8px 25px rgba(106,27,154,0.4);
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
        box-shadow: 0 10px 40px rgba(0,0,0,0.25);
        transition: transform 0.3s;
    }}
    .kpi-card:hover {{
        transform: translateY(-8px);
    }}
    .kpi-title {{
        font-size: 1.3rem;
        color: #94a3b8;
        margin-bottom: 12px;
    }}
    .kpi-value {{
        font-size: 3.2rem;
        font-weight: 800;
        color: {ACCENT_YELLOW};
        margin: 8px 0;
    }}
    .kpi-delta {{
        font-size: 1.1rem;
        color: #10b981;
    }}
    .modal {{
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.4s;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    .modal-content {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px;
        max-width: 420px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        animation: slideUp 0.5s;
    }}
    @keyframes slideUp {{
        from {{ transform: translateY(60px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    .login-input {{
        width: 100%;
        padding: 14px;
        margin: 12px 0;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.06);
        color: white;
    }}
    .login-btn {{
        width: 100%;
        padding: 16px;
        background: linear-gradient(45deg, {VIOLET}, {ACCENT_VIOLET});
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 20px;
    }}

    /* ───────────────────────────────────────────────────────────────
       PATCH VISIBILITÉ FILTRES (selectbox) — VILLES EN JAUNE
       ─────────────────────────────────────────────────────────────── */
    div[data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        color: {YELLOW} !important;
    }}

    div[data-baseweb="select"] div[role="button"] {{
        color: {YELLOW} !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="select"] input {{
        color: {YELLOW} !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="menu"] {{
        background-color: {card_bg} !important;
        color: {YELLOW} !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        backdrop-filter: blur(10px) !important;
    }}

    div[data-baseweb="option"] {{
        color: {YELLOW} !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="option"]:hover {{
        background-color: rgba(253,209,0,0.18) !important;
    }}

</style>
""", unsafe_allow_html=True)
# ─── Barre du haut ──────────────────────────────────────────────────────────────
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=70)

with col_title:
    st.markdown(f"""
        <h1 style="margin:0; text-align:center; font-size:2.6rem;">
            PARIS <span style="color:{YELLOW};">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#94a3b8; margin:4px 0 0;">
            Communauté d'agglomération
        </p>
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
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Contenu par page ───────────────────────────────────────────────────────────
st.markdown("<div class='main'>", unsafe_allow_html=True)

# ========== ACCUEIL ==========
if current_theme == "Accueil":

    st.markdown("<h1 style='text-align:center; margin-bottom:40px; color:white;'>Bienvenue sur l'Observatoire</h1>", unsafe_allow_html=True)

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

# ========== POPULATION ==========
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

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            animated_kpi("Population totale", int(df_filtre["Valeur"].sum()), annee)
        with col2:
            animated_kpi("Moins de 20 ans", 145000, "jeunes")
        with col3:
            animated_kpi("65 ans et plus", 98000, "seniors")
        with col4:
            animated_kpi("Croissance", "2.8 %", "annuelle")

        st.markdown("</div>", unsafe_allow_html=True)

        fig = px.bar(df_filtre.head(10), x="Géographie", y="Valeur",
                     title="Population par commune")
        st.plotly_chart(fig, use_container_width=True)

# ========== EMPLOI / CHÔMAGE ==========
elif current_theme == "Emploi / Chômage":

    chomage = load_data("POP_CHOMAGE_DARES.csv")
    secteur = load_data("POP_ACTIF_OCCUPE_PCS_SECTEUR.csv")
    diplome = load_data("POP_ACTIF_INACTIF_DIPLOME.csv")

    if not chomage.empty:
        chomage = chomage.rename(columns=lambda x: x.strip())

        st.subheader("Filtres")
        c1, c2 = st.columns(2)

        with c1:
            annees = sorted(chomage["Date"].str[:4].unique())
            annee = st.selectbox("Année", annees, index=len(annees)-1)
        with c2:
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
            animated_kpi("Prof. intermédiaires", "37 776", "2011")

        st.markdown("</div>", unsafe_allow_html=True)

        evol = chomage.groupby("Date")["Nombre de demandeurs d'emploi"].sum().reset_index()
        st.plotly_chart(
            px.line(evol, x="Date", y="Nombre de demandeurs d'emploi",
                    title="Évolution du nombre de demandeurs d'emploi"),
            use_container_width=True
        )

        age = df_chom.groupby("Tranche d'âge")["Nombre de demandeurs d'emploi"].sum().reset_index()
        st.plotly_chart(
            px.pie(age, values="Nombre de demandeurs d'emploi", names="Tranche d'âge",
                   title="Répartition par âge"),
            use_container_width=True
        )

    if not secteur.empty:
        top = secteur.groupby("Activité économique des emplois")["Valeur"].sum().nlargest(5).reset_index()
        st.plotly_chart(
            px.bar(top, x="Activité économique des emplois", y="Valeur",
                   title="Top 5 secteurs d'emploi"),
            use_container_width=True
        )

    if not diplome.empty:
        dist = diplome.groupby("Diplôme")["Valeur"].sum().reset_index()
        st.plotly_chart(
            px.pie(dist, values="Valeur", names="Diplôme", title="Actifs par diplôme"),
            use_container_width=True
        )

# ========== ÉCONOMIE ==========
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
        st.plotly_chart(
            px.line(grp, x="Période", y="Valeur",
                    title="Évolution des créations d'entreprises"),
            use_container_width=True
        )

# ========== SOCIAL / MÉNAGES ==========
elif current_theme == "Social / Ménages":

    df = load_data("POP_MENAGES.csv")

    if not df.empty:

        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            animated_kpi("Ménages monoparentaux", "18.7 %", "2021")
        with c2:
            animated_kpi("Taille moyenne ménage", "2.4", "stable")
        with c3:
            animated_kpi("Revenu médian", "27 650 €", "2021")
        with c4:
            animated_kpi("Taux pauvreté", "10.1 %", "2021")

        st.markdown("</div>", unsafe_allow_html=True)

        st.plotly_chart(
            px.bar(df.head(10), x="Géographie", y="Valeur",
                   title="Ménages par commune"),
            use_container_width=True
        )

# ========== ÉDUCATION ==========
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

        st.plotly_chart(
            px.pie(df.head(10), values="Valeur", names="Diplôme",
                   title="Répartition des diplômes"),
            use_container_width=True
        )
# ========== SPORTS ==========
elif current_theme == "Sports":

    st.markdown("<h2 style='text-align:center;'>Sports</h2>", unsafe_allow_html=True)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        animated_kpi("Clubs sportifs", "312", "2025")
    with c2:
        animated_kpi("Équipements sportifs", "198", "Agglomération")
    with c3:
        animated_kpi("Pratique régulière", "64 %", "habitants")
    with c4:
        animated_kpi("Événements/an", "148", "sportifs")

    st.markdown("</div>", unsafe_allow_html=True)
    st.info("Contenu Sports en cours d’enrichissement.")


# ========== FINANCE (MODAL ORIGINALE) ==========
elif current_theme == "Finance":

    if "finance_open" not in st.session_state:
        st.session_state.finance_open = False

    if st.button("Accéder à Finance", type="primary"):
        st.session_state.finance_open = True

    if st.session_state.finance_open:

        st.markdown(f"""
<div class="modal">
    <div class="modal-content">

        <h2 style="color:{YELLOW}; text-align:center;">Finance</h2>

        <input class="login-input" placeholder="Identifiant" style="color:white;">

        <input class="login-input" type="password" placeholder="Mot de passe" style="color:white;">

        <button class="login-btn">Se connecter</button>

        <p style="text-align:center; margin-top:20px; color:white;">
            #Mot de passe oublié ?</a>
        </p>

    </div>
</div>
""", unsafe_allow_html=True)

# ========== PAGE PAR DÉFAUT ==========
else:

    st.markdown(f"<h2 style='text-align:center;'>{current_theme}</h2>", unsafe_allow_html=True)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    cols = st.columns(4)

    for i, col in enumerate(cols):
        with col:
            animated_kpi(f"Indicateur {i+1}", "12 345", "+X %")

    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Contenu {current_theme} en cours de développement.")

# Fin du conteneur principal
st.markdown("</div>", unsafe_allow_html=True)


# ========== FOOTER ==========
st.markdown("""
<div style="text-align:center; color:#94a3b8; margin:100px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 |
    Développé par la communauté d'agglomération Paris-Saclay
</div>
""", unsafe_allow_html=True)
