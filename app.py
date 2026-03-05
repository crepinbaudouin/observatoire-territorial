# app.py - Observatoire Territorial Paris-Saclay - Avec données emploi/chômage réelles
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
            background: linear-gradient(to bottom, rgba(15,23,42,0.45), rgba(15,23,42,0.65));
            z-index: -1;
        }}
        h1, h2, h3, p {{
            text-shadow: 0 3px 12px rgba(0,0,0,0.9) !important;
            color: #ffffff !important;
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
            font-size: 2.8rem;
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
        @media (max-width: 768px) {{
            .kpi-container {{
                grid-template-columns: 1fr;
            }}
            .kpi-value {{
                font-size: 2.8rem;
            }}
            .nav-tabs {{
                flex-direction: column;
                align-items: center;
            }}
            .header {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Barre du haut ──────────────────────────────────────────────────────────────
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

# ─── Page Accueil ───────────────────────────────────────────────────────────────
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

# ─── Page Emploi / Chômage ─────────────────────────────────────────────────────
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

    # Filtrage chômage
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

    # Emplois occupés (dernière période totale)
    emplois_total = 0
    if not actif_secteur.empty:
        emplois_total = int(actif_secteur[
            (actif_secteur["Profession et catégorie socioprofessionnelle (PCS)"] == "Total") &
            (actif_secteur["Forme d'emploi"] == "Total") &
            (actif_secteur["Activité économique des emplois"] == "Total") &
            (actif_secteur["Sexe"] == "Total")
        ]["Valeur"].iloc[-1])

    # Taux approximatif
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

    # Graphiques
    if not df_chom.empty:
        fig_evol = px.line(chomage.groupby("Date")["Nombre de demandeurs d'emploi"].sum().reset_index(),
                           x="Date", y="Nombre de demandeurs d'emploi",
                           title="Évolution demandeurs d'emploi (toutes communes)")
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

    # Filtrage des données
    df_stocks = stocks.copy()
    df_stocks = df_stocks[df_stocks["Période"] == periode_sel]
    if activite_sel != "Toutes":
        df_stocks = df_stocks[df_stocks["Activité économique"] == activite_sel]

    # KPI réels
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
            
            # Filtre sur la mesure "Effectifs"
            effectifs_df = df_flores[df_flores["Mesures de Flores"] == "Effectifs présents la dernière semaine de décembre"]
            effectif_total = int(effectifs_df["Valeur"].sum()) if not effectifs_df.empty else 0
            
            animated_kpi("Effectifs salariés", f"{effectif_total:,}", f"{periode_sel}")
        else:
            animated_kpi("Effectifs salariés", "N/A", "données manquantes")

    with col4:
        animated_kpi("Taux de création estimé", "N/A", "(données complémentaires nécessaires)")

    st.markdown("</div>", unsafe_allow_html=True)

    # Graphiques Plotly
    if not df_stocks.empty:
        # 1. Évolution du nombre d'établissements (toutes activités)
        evol_etab = stocks.groupby("Période")["Valeur"].sum().reset_index()
        fig_evol = px.line(evol_etab, x="Période", y="Valeur",
                           title="Évolution du nombre d'établissements",
                           markers=True)
        st.plotly_chart(fig_evol, use_container_width=True)

        # 2. Top 5 activités économiques (dernière période)
        top_activ = df_stocks.groupby("Activité économique")["Valeur"].sum().nlargest(5).reset_index()
        fig_activ = px.bar(top_activ, x="Activité économique", y="Valeur",
                           title="Top 5 activités économiques (établissements)",
                           color="Valeur", color_continuous_scale="Viridis")
        fig_activ.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_activ, use_container_width=True)

    if not flores.empty:
        # 3. Répartition par taille d'établissement (dernière période)
        taille_dist = flores[flores["Période"] == periode_sel].groupby("Taille en tranches d'effectifs")["Établissements"].sum().reset_index()
        fig_taille = px.pie(taille_dist, values="Établissements", names="Taille en tranches d'effectifs",
                            title="Répartition des établissements par taille")
        st.plotly_chart(fig_taille, use_container_width=True)

    if not creations.empty:
        # 4. Évolution des créations d'entreprises
        evol_crea = creations.groupby("Période")["Valeur"].sum().reset_index()
        fig_crea = px.line(evol_crea, x="Période", y="Valeur",
                           title="Évolution des créations d'entreprises",
                           markers=True)
        st.plotly_chart(fig_crea, use_container_width=True)
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

# Footer
st.markdown("""
<div style="text-align:center; color:#94a3b8; margin:100px 0 40px; font-size:0.95rem;">
    © Communauté Paris-Saclay | Données février 2026 | Développé avec Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
