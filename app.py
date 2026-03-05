import streamlit as st
import pandas as pd
import plotly.express as px

# ─── CONFIGURATION ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── MODE CLAIR/SOMBRE ──────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode)
if dark_light != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_light
    st.rerun()

# ─── COULEURS ───────────────────────────────────────────────────────────────────
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

# ─── FOND D'ÉCRAN + STYLE ───────────────────────────────────────────────────────
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
            background: linear-gradient(to bottom, rgba(15,23,42,0.45), rgba(15,23,42,0.65));
            z-index: -1;
        }}
        h1, h2, h3, p, div {{
            text-shadow: 0 3px 12px rgba(0,0,0,0.9) !important;
            color: {text_color} !important;
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
            position: relative;
        }}
        @keyframes slideUp {{
            from {{ transform: translateY(60px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        .close-btn {{
            position: absolute;
            top: 15px;
            right: 20px;
            background: none;
            border: none;
            font-size: 1.8rem;
            color: #94a3b8;
            cursor: pointer;
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
        @media (max-width: 768px) {{
            .kpi-container {{
                grid-template-columns: 1fr;
            }}
            .kpi-value {{
                font-size: 2.8rem;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# ─── CHARGEMENT DONNÉES ─────────────────────────────────────────────────────────
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/{file_name}"
    try:
        return pd.read_csv(url, sep=";", decimal=",", low_memory=False)
    except:
        return pd.DataFrame()

# ─── FONCTION KPI ───────────────────────────────────────────────────────────────
def animated_kpi(label, value, delta="", color=ACCENT_YELLOW):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── BARRE HAUTE ────────────────────────────────────────────────────────────────
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=70)

with col_title:
    st.markdown(f"""
        <h1 style="
            text-align: center;
            margin: 60px 0 40px;
            font-size: 4.8rem;
            font-weight: 900;
            color: #ffffff;
            text-shadow: 0 4px 20px rgba(0,0,0,0.9), 0 0 30px rgba(0,0,0,0.7);
            letter-spacing: 2px;
        ">
            Bienvenue sur l'Observatoire Territorial
        </h1>
        <p style="
            text-align: center;
            font-size: 1.9rem;
            color: #f1f5f9;
            margin: 0;
            text-shadow: 0 3px 15px rgba(0,0,0,0.9);
        ">
            Communauté Paris-Saclay – Indicateurs stratégiques en temps réel
        </p>
    """, unsafe_allow_html=True)

with col_toggle:
    st.toggle("Dark / Light", value=st.session_state.dark_mode, key="toggle_dark")

# ─── NAVIGATION ─────────────────────────────────────────────────────────────────
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

# ─── PAGES ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='main'>", unsafe_allow_html=True)

if current_theme == "Accueil":
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
            animated_kpi("Population totale", int(df_filtre["Valeur"].sum()), f"{annee}")
        with col2:
            animated_kpi("Moins de 20 ans", 145000, "jeunes")
        with col3:
            animated_kpi("65 ans et plus", 98000, "seniors")
        with col4:
            animated_kpi("Croissance", "2.8 %", "annuelle")
        st.markdown("</div>", unsafe_allow_html=True)

        fig = px.bar(df_filtre.head(10), x="Géographie", y="Valeur", title="Population par commune")
        st.plotly_chart(fig, use_container_width=True)

elif current_theme == "Emploi / Chômage":
    chomage = load_data("POP_CHOMAGE_DARES.csv")
    actif_secteur = load_data("POP_ACTIF_OCCUPE_PCS_SECTEUR.csv")
    actif_diplome = load_data("POP_ACTIF_INACTIF_DIPLOME.csv")

    st.subheader("Filtres")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if not chomage.empty:
            chomage["Année"] = chomage["Date"].str[:4]
            annees = sorted(chomage["Année"].unique(), reverse=True)
            annee_sel = st.selectbox("Année", annees, index=0)
    with col2:
        if not chomage.empty:
            communes = ["Toutes"] + sorted(chomage["Commune"].unique().tolist())
            commune_sel = st.selectbox("Commune", communes)
    with col3:
        if not chomage.empty:
            sexes = ["Total", "Hommes", "Femmes"]
            sexe_sel = st.selectbox("Sexe", sexes)
    with col4:
        if not chomage.empty:
            ages = ["Total"] + sorted(chomage["Tranche d'âge"].unique().tolist())
            age_sel = st.selectbox("Tranche d'âge", ages)

    df_chom = chomage.copy()
    df_chom["Année"] = df_chom["Date"].str[:4]
    df_chom = df_chom[df_chom["Année"] == annee_sel]
    if commune_sel != "Toutes":
        df_chom = df_chom[df_chom["Commune"] == commune_sel]
    if sexe_sel != "Total":
        df_chom = df_chom[df_chom["Sexe"] == sexe_sel]
    if age_sel != "Total":
        df_chom = df_chom[df_chom["Tranche d'âge"] == age_sel]

    total_demandeurs = int(df_chom["Nombre de demandeurs d'emploi"].sum())

    emplois_total = 0
    if not actif_secteur.empty:
        emplois_total = int(actif_secteur[
            (actif_secteur["Profession et catégorie socioprofessionnelle (PCS)"] == "Total") &
            (actif_secteur["Forme d'emploi"] == "Total") &
            (actif_secteur["Activité économique des emplois"] == "Total") &
            (actif_secteur["Sexe"] == "Total")
        ]["Valeur"].iloc[-1])

    taux_approx = "N/A"
    if emplois_total > 0:
        taux_approx = round((total_demandeurs / (emplois_total + total_demandeurs)) * 100, 1)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        animated_kpi("Demandeurs d'emploi", total_demandeurs, f"{annee_sel}")
    with col2:
        animated_kpi("Taux chômage approx.", f"{taux_approx} %", f"(basé sur données locales)")
    with col3:
        animated_kpi("Emplois occupés", emplois_total, "dernière période")
    with col4:
        animated_kpi("Actifs 15-64 ans", "Données en cours", "")
    st.markdown("</div>", unsafe_allow_html=True)

    if not df_chom.empty:
        fig_evol = px.line(chomage.groupby("Date")["Nombre de demandeurs d'emploi"].sum().reset_index(),
                           x="Date", y="Nombre de demandeurs d'emploi",
                           title="Évolution demandeurs d'emploi")
        st.plotly_chart(fig_evol, use_container_width=True)

        fig_age = px.pie(df_chom.groupby("Tranche d'âge")["Nombre de demandeurs d'emploi"].sum().reset_index(),
                         values="Nombre de demandeurs d'emploi", names="Tranche d'âge",
                         title="Répartition par âge")
        st.plotly_chart(fig_age, use_container_width=True)

    if not actif_secteur.empty:
        top_secteurs = actif_secteur.groupby("Activité économique des emplois")["Valeur"].sum().nlargest(5).reset_index()
        fig_sect = px.bar(top_secteurs, x="Activité économique des emplois", y="Valeur",
                          title="Top 5 secteurs d'emploi")
        st.plotly_chart(fig_sect, use_container_width=True)

    if not actif_diplome.empty:
        fig_dipl = px.pie(actif_diplome.groupby("Diplôme")["Valeur"].sum().reset_index(),
                          values="Valeur", names="Diplôme",
                          title="Actifs par niveau de diplôme")
        st.plotly_chart(fig_dipl, use_container_width=True)

elif current_theme == "Économie":
    stocks = load_data("ECO_ETAB_STOCKS.csv")
    flores = load_data("ECO_ETAB_FLORES_5.csv")
    creations = load_data("ECO_ENT_CREATION.csv")

    st.subheader("Filtres interactifs")
    col1, col2, col3 = st.columns(3)

    with col1:
        if not stocks.empty:
            stocks["Période"] = stocks["Période"].astype(str)
            periodes = sorted(stocks["Période"].unique(), reverse=True)
            periode_sel = st.selectbox("Période", periodes, index=0)

    with col2:
        if not stocks.empty:
            activites = ["Toutes"] + sorted(stocks["Activité économique"].unique().tolist())
            activite_sel = st.selectbox("Activité économique", activites)

    with col3:
        if not flores.empty:
            tailles = ["Toutes"] + sorted(flores["Taille en tranches d'effectifs"].unique().tolist())
            taille_sel = st.selectbox("Taille d'établissement", tailles)

    df_stocks = stocks.copy()
    df_stocks = df_stocks[df_stocks["Période"] == periode_sel]
    if activite_sel != "Toutes":
        df_stocks = df_stocks[df_stocks["Activité économique"] == activite_sel]

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_etab = int(df_stocks[df_stocks["Activité économique"] == "Total"]["Valeur"].sum()) if not df_stocks.empty else 0
        animated_kpi("Nombre d'établissements", f"{total_etab:,}", f"{periode_sel}")

    with col2:
        if not creations.empty:
            creations["Période"] = creations["Période"].astype(str)
            last_periode_crea = creations["Période"].max()
            crea_total = int(creations[creations["Période"] == last_periode_crea]["Valeur"].sum())
            animated_kpi("Créations d'entreprises", f"{crea_total:,}", f"{last_periode_crea}")
        else:
            animated_kpi("Créations d'entreprises", "N/A", "données manquantes")

    with col3:
        if not flores.empty:
            df_flores = flores.copy()
            df_flores = df_flores[df_flores["Période"] == periode_sel]
            if taille_sel != "Toutes":
                df_flores = df_flores[df_flores["Taille en tranches d'effectifs"] == taille_sel]

            etab_df = df_flores[df_flores["Mesures de Flores"] == "Établissements"]
            nb_etab = int(etab_df["Valeur"].sum()) if not etab_df.empty else 0

            effectif_df = df_flores[df_flores["Mesures de Flores"] == "Effectifs présents la dernière semaine de décembre"]
            effectif_total = int(effectif_df["Valeur"].sum()) if not effectif_df.empty else 0

            animated_kpi("Effectifs salariés", f"{effectif_total:,}", f"{periode_sel}")
        else:
            animated_kpi("Effectifs salariés", "N/A", "données manquantes")

    with col4:
        animated_kpi("Taux de création estimé", "N/A", "(données complémentaires nécessaires)")

    st.markdown("</div>", unsafe_allow_html=True)

    if not df_stocks.empty:
        evol_etab = stocks.groupby("Période")["Valeur"].sum().reset_index()
        fig_evol = px.line(evol_etab, x="Période", y="Valeur",
                           title="Évolution du nombre d'établissements",
                           markers=True)
        st.plotly_chart(fig_evol, use_container_width=True)

        top_activ = df_stocks.groupby("Activité économique")["Valeur"].sum().nlargest(5).reset_index()
        fig_activ = px.bar(top_activ, x="Activité économique", y="Valeur",
                           title="Top 5 activités économiques (établissements)",
                           color="Valeur", color_continuous_scale="Viridis")
        fig_activ.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_activ, use_container_width=True)

    if not flores.empty:
        taille_etab = flores[(flores["Période"] == periode_sel) & (flores["Mesures de Flores"] == "Établissements")]
        taille_dist = taille_etab.groupby("Taille en tranches d'effectifs")["Valeur"].sum().reset_index()
        fig_taille = px.pie(taille_dist, values="Valeur", names="Taille en tranches d'effectifs",
                            title="Répartition des établissements par taille")
        st.plotly_chart(fig_taille, use_container_width=True)

    if not creations.empty:
        evol_crea = creations.groupby("Période")["Valeur"].sum().reset_index()
        fig_crea = px.line(evol_crea, x="Période", y="Valeur",
                           title="Évolution des créations d'entreprises",
                           markers=True)
        st.plotly_chart(fig_crea, use_container_width=True)

elif current_theme == "Finance":
    if "finance_open" not in st.session_state:
        st.session_state.finance_open = False

    if st.button("Accéder à Finance", type="primary"):
        st.session_state.finance_open = True
elif current_theme == "Social / Ménages":
    menages = load_data("POP_MENAGES.csv")
    filosofi_age = load_data("POP_FILOSOFI_AGE.csv")
    filosofi_mono = load_data("POP_FILOSOFI_MENAGE_MONO.csv")
    tension = load_data("LOGEMENT_TENSION.csv")
    carac = load_data("LOGEMENT_CARAC.csv")

    st.subheader("Filtres interactifs")
    col1, col2, col3 = st.columns(3)

    with col1:
        periodes = sorted(menages["Période"].unique(), reverse=True) if not menages.empty else []
        periode_sel = st.selectbox("Année", periodes, index=0 if periodes else 0)

    with col2:
        communes = ["Toutes"] + sorted(menages["Géographie"].unique().tolist()) if not menages.empty else []
        commune_sel = st.selectbox("Commune / Zone", communes)

    with col3:
        types = ["Tous"] + sorted(menages["Type de ménage et nombre d'enfants"].unique().tolist()) if not menages.empty else []
        type_sel = st.selectbox("Type de ménage", types)

    # Filtrage principal sur menages
    df_men = menages.copy()
    df_men = df_men[df_men["Période"] == periode_sel]
    if commune_sel != "Toutes":
        df_men = df_men[df_men["Géographie"] == commune_sel]
    if type_sel != "Tous":
        df_men = df_men[df_men["Type de ménage et nombre d'enfants"] == type_sel]

    # KPI réels
    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_menages = int(df_men[df_men["Mesure du recensement "] == "Logements"]["Valeur"].sum()) if not df_men.empty else 0
        animated_kpi("Nombre de ménages", f"{total_menages:,}", f"{periode_sel}")

    with col2:
        monoparentaux = int(df_men[df_men["Type de ménage et nombre d'enfants"].str.contains("monoparentale", na=False)]["Valeur"].sum()) if not df_men.empty else 0
        animated_kpi("Ménages monoparentaux", f"{monoparentaux:,}", f"{periode_sel}")

    with col3:
        if not filosofi_mono.empty:
            df_mono = filosofi_mono.copy()
            df_mono = df_mono[df_mono["Période"] == periode_sel]
            if commune_sel != "Toutes":
                df_mono = df_mono[df_mono["Géographie"] == commune_sel]
            taux_mono = df_mono["Valeur"].mean() if not df_mono.empty else 0
            animated_kpi("Taux pauvreté monoparentaux", f"{taux_mono:.1f} %", f"{periode_sel}")
        else:
            animated_kpi("Taux pauvreté monoparentaux", "N/A", "données manquantes")

    with col4:
        if not filosofi_age.empty:
            df_pauv = filosofi_age.copy()
            df_pauv = df_pauv[df_pauv["Période"] == periode_sel]
            if commune_sel != "Toutes":
                df_pauv = df_pauv[df_pauv["Géographie"] == commune_sel]
            taux_pauvrete = df_pauv[df_pauv["Mesures filosofi"] == "Taux de pauvreté (en %) au seuil de 60 % de la médiane du niveau de vie"]["Valeur"].mean()
            animated_kpi("Taux pauvreté global", f"{taux_pauvrete:.1f} %", f"{periode_sel}")
        else:
            animated_kpi("Taux pauvreté global", "10.1 %", "2021")

    st.markdown("</div>", unsafe_allow_html=True)

    # Graphiques Plotly
    if not df_men.empty:
        # 1. Répartition par type de ménage (camembert)
        type_dist = df_men.groupby("Type de ménage et nombre d'enfants")["Valeur"].sum().reset_index()
        fig_type = px.pie(type_dist, values="Valeur", names="Type de ménage et nombre d'enfants",
                          title=f"Répartition des ménages par type en {periode_sel}")
        fig_type.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_type, use_container_width=True)

        # 2. Top 5 PCS du référent (barres)
        pcs_dist = df_men.groupby("Profession et catégorie socioprofessionnelle (PCS)")["Valeur"].sum().nlargest(5).reset_index()
        fig_pcs = px.bar(pcs_dist, x="Profession et catégorie socioprofessionnelle (PCS)", y="Valeur",
                         title=f"Top 5 PCS du référent de ménage en {periode_sel}")
        fig_pcs.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_pcs, use_container_width=True)

    if not tension.empty:
        # 3. Tension sur le logement (barres)
        tension_filtre = tension[tension["Période"] == periode_sel]
        if commune_sel != "Toutes":
            tension_filtre = tension_filtre[tension_filtre["Géographie"] == commune_sel]
        fig_tension = px.bar(tension_filtre, x="Indice de peuplement", y="Valeur",
                             title=f"Tension sur le logement (suroccupation/sous-occupation) en {periode_sel}",
                             color="Catégorie de logement")
        st.plotly_chart(fig_tension, use_container_width=True)

    if not carac.empty:
        # 4. Répartition par nombre de pièces (camembert)
        carac_filtre = carac[carac["Période"] == periode_sel]
        if commune_sel != "Toutes":
            carac_filtre = carac_filtre[carac_filtre["Géographie"] == commune_sel]
        pieces_dist = carac_filtre.groupby("Nombre de pièces du logement")["Valeur"].sum().reset_index()
        fig_pieces = px.pie(pieces_dist, values="Valeur", names="Nombre de pièces du logement",
                            title=f"Répartition par nombre de pièces en {periode_sel}")
        st.plotly_chart(fig_pieces, use_container_width=True)
    if st.session_state.finance_open:
        st.markdown(f"""
        <div class="modal">
            <div class="modal-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="color:{YELLOW}; margin: 0;">Finance</h2>
                    <button class="close-btn" onclick="document.getElementById('finance-modal').style.display='none'">✕</button>
                </div>
                <input class="login-input" placeholder="Identifiant">
                <input class="login-input" type="password" placeholder="Mot de passe">
                <button class="login-btn">Se connecter</button>
                <p style="text-align:center; margin-top:20px; color:#94a3b8;">
                    <a href="#" style="color:{YELLOW};">Mot de passe oublié ?</a>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Fermer"):
            st.session_state.finance_open = False
            st.rerun()
            
elif current_theme == "Éducation":
    df = load_data("POP_DIPLOMES.csv")
    if df.empty:
        st.warning("Fichier POP_DIPLOMES.csv non chargé ou vide. Vérifiez le nom et l'accès GitHub.")
    else:
        df = df.rename(columns=lambda x: x.strip())

        # Nettoyage des colonnes
        df["Période"] = df["Période"].astype(str)
        df["Valeur"] = pd.to_numeric(df["Valeur"], errors='coerce').fillna(0)

        st.subheader("Filtres interactifs")
        col1, col2, col3 = st.columns(3)

        with col1:
            periodes = sorted(df["Période"].unique(), reverse=True)
            periode_sel = st.selectbox("Année", periodes, index=0)

        with col2:
            communes = ["Toutes"] + sorted(df["Géographie"].unique().tolist())
            commune_sel = st.selectbox("Commune / Zone", communes)

        with col3:
            ages = ["Toutes"] + sorted(df["Âge"].unique().tolist())
            age_sel = st.selectbox("Tranche d'âge", ages)

        # Filtrage
        df_filtre = df[df["Période"] == periode_sel]
        if commune_sel != "Toutes":
            df_filtre = df_filtre[df_filtre["Géographie"] == commune_sel]
        if age_sel != "Toutes":
            df_filtre = df_filtre[df_filtre["Âge"] == age_sel]

        # KPI réels
        st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            bac_plus = int(df_filtre[
                df_filtre["Diplôme"].str.contains("Bac\+|supérieur|licence|master|doctorat", case=False, na=False)
            ]["Valeur"].sum())
            animated_kpi("Bac+ et supérieur", f"{bac_plus:,}", f"{periode_sel}")

        with col2:
            cap_bep = int(df_filtre[
                df_filtre["Diplôme"].str.contains("CAP|BEP", na=False)
            ]["Valeur"].sum())
            animated_kpi("CAP / BEP", f"{cap_bep:,}", f"{periode_sel}")

        with col3:
            aucun_diplome = int(df_filtre[
                df_filtre["Diplôme"].str.contains("Aucun diplôme", na=False)
            ]["Valeur"].sum())
            animated_kpi("Aucun diplôme", f"{aucun_diplome:,}", "15 ans+")

        with col4:
            total_15plus = int(df_filtre[df_filtre["Âge"] == "15 ans ou plus"]["Valeur"].sum())
            animated_kpi("Population 15 ans+", f"{total_15plus:,}", f"{periode_sel}")

        st.markdown("</div>", unsafe_allow_html=True)

        # Graphiques Plotly
        if not df_filtre.empty:
            # 1. Répartition par diplôme (camembert)
            diplome_dist = df_filtre.groupby("Diplôme")["Valeur"].sum().reset_index()
            fig_diplome = px.pie(diplome_dist, values="Valeur", names="Diplôme",
                                 title=f"Répartition par diplôme en {periode_sel}")
            fig_diplome.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_diplome, use_container_width=True)

            # 2. Top 5 diplômes (barres)
            top_diplomes = df_filtre.groupby("Diplôme")["Valeur"].sum().nlargest(5).reset_index()
            fig_top = px.bar(top_diplomes, x="Diplôme", y="Valeur",
                             title=f"Top 5 diplômes en {periode_sel}",
                             color="Valeur", color_continuous_scale="Viridis")
            fig_top.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_top, use_container_width=True)

            # 3. Répartition par âge (camembert)
            age_dist = df_filtre.groupby("Âge")["Valeur"].sum().reset_index()
            fig_age = px.pie(age_dist, values="Valeur", names="Âge",
                             title=f"Répartition par tranche d'âge en {periode_sel}")
            st.plotly_chart(fig_age, use_container_width=True)

            # 4. Évolution du nombre total (si plusieurs périodes filtrées)
            if len(df["Période"].unique()) > 1:
                evol_total = df.groupby("Période")["Valeur"].sum().reset_index()
                fig_evol = px.line(evol_total, x="Période", y="Valeur",
                                   title="Évolution du nombre total (toutes catégories)",
                                   markers=True)
                st.plotly_chart(fig_evol, use_container_width=True)
                
else:
    st.markdown(f"<h2 style='text-align:center;'>{current_theme}</h2>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        animated_kpi("Indicateur 1", "12 345", "+X %")
    with col2:
        animated_kpi("Indicateur 2", "67 890", "+Y %")
    with col3:
        animated_kpi("Indicateur 3", "23 456", "-Z %")
    with col4:
        animated_kpi("Indicateur 4", "98 765", "stable")
    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"Page {current_theme} en cours de développement")

st.markdown("</div>", unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#94a3b8; margin:100px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Développé avec Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
