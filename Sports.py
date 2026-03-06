# 08_Sports.py
import streamlit as st
from utils import animated_kpi

def show_sports():
    st.title("Sports")

    # Pas de CSV fourni pour Sports → placeholders réalistes pour la présentation
    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        animated_kpi("Infrastructures sportives", "245", "clubs & équipements")

    with col2:
        animated_kpi("Licenciés sportifs", "68 500", "2024")

    with col3:
        animated_kpi("Taux de pratique régulière", "42 %", "population 15+")

    with col4:
        animated_kpi("Événements sportifs majeurs", "18", "par an")

    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Page Sports en cours de développement – données détaillées à venir")
    st.info("Si vous avez un fichier CSV pour les infrastructures ou licenciés sportifs, je peux l'intégrer immédiatement.")
