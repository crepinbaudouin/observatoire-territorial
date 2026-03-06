# 07_Éducation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_education():
    st.title("Éducation")

    df = load_data("POP_DIPLOMES.csv")
    if df.empty:
        st.warning("Fichier POP_DIPLOMES.csv non chargé ou vide")
        return

    df = df.rename(columns=lambda x: x.strip())
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

    # Graphiques
    if not df_filtre.empty:
        # Répartition par diplôme (camembert)
        diplome_dist = df_filtre.groupby("Diplôme")["Valeur"].sum().reset_index()
        fig_diplome = px.pie(diplome_dist, values="Valeur", names="Diplôme",
                             title=f"Répartition par diplôme en {periode_sel}")
        fig_diplome.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_diplome, use_container_width=True)

        # Top 5 diplômes (barres)
        top_diplomes = df_filtre.groupby("Diplôme")["Valeur"].sum().nlargest(5).reset_index()
        fig_top = px.bar(top_diplomes, x="Diplôme", y="Valeur",
                         title=f"Top 5 diplômes en {periode_sel}",
                         color="Valeur", color_continuous_scale="Viridis")
        fig_top.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_top, use_container_width=True)

        # Répartition par âge (camembert)
        age_dist = df_filtre.groupby("Âge")["Valeur"].sum().reset_index()
        fig_age = px.pie(age_dist, values="Valeur", names="Âge",
                         title=f"Répartition par tranche d'âge en {periode_sel}")
        st.plotly_chart(fig_age, use_container_width=True)
