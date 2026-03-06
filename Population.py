# 02_Population.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_population():
    st.title("Population")

    df = load_data("POP_RECENSEMENT.csv")
    if df.empty:
        st.warning("Fichier POP_RECENSEMENT.csv non chargé ou vide")
        return

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
