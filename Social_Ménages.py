# Social_Ménages.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_social_menages():
    st.title("Social / Ménages")

    menages = load_data("POP_MENAGES.csv")
    # ... charge les autres fichiers comme avant

    # Ton code complet de la page Social / Ménages ici (filtres, KPI, graphiques)
    # Exemple simplifié :
    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        animated_kpi("Nombre de ménages", "45 678", "2022")
    with col2:
        animated_kpi("Ménages monoparentaux", "8 912", "19.5 %")
    with col3:
        animated_kpi("Taux pauvreté", "10.1 %", "2021")
    with col4:
        animated_kpi("Revenu médian", "27 650 €", "2021")
    st.markdown("</div>", unsafe_allow_html=True)

    # Ajoute tes graphiques, filtres, etc.
