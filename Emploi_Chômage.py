# 03_Emploi_Chômage.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_emploi_chomage():
    # Fond d'écran spécifique à la page Emploi/Chômage
    bg_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/emploi.jpeg"

    st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background-image: url("{bg_url}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            [data-testid="stAppViewContainer"] > div:first-child::before {{
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(to bottom, rgba(15,23,42,0.55), rgba(15,23,42,0.75));
                z-index: -1;
                pointer-events: none;
            }}
            h1, h2, h3, p, label, .stSelectbox label, .stMarkdown {{
                color: #ffffff !important;
                text-shadow: 0 2px 8px rgba(0,0,0,0.9) !important;
            }}
            .block-container, .st-emotion-cache-1r6slb0 {{
                background: transparent !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.title("Emploi / Chômage")

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

    # Filtrage
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
