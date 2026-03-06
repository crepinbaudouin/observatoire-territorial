# 04_Économie.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_economie():
    # Fond d'écran spécifique à la page Économie
    bg_url = "https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/economie.jpg"

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

    st.title("Économie")

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

    # Filtrage des données stocks
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

    # Graphiques Plotly
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
