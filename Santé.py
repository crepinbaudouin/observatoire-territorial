# Santé.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, animated_kpi

def show_sante():
    st.title("Santé")

    # Pour l'instant, on n'a pas de fichier CSV spécifique "Santé" dans les documents fournis
    # Donc on affiche des placeholders réalistes + un message d'attente pour les données
    # Si tu as un fichier (ex: santé.csv, morbidité, espérance de vie, etc.), envoie-le-moi pour l'intégrer

    st.markdown("""
    <div style="text-align:center; margin:40px 0; color:#94a3b8;">
        <h3>Données santé en cours de chargement</h3>
        <p>Indicateurs de santé publique, espérance de vie, morbidité, accès aux soins, etc.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        animated_kpi("Espérance de vie", "82.4 ans", "2023")

    with col2:
        animated_kpi("Taux de vaccination DTP", "94 %", "enfants 2 ans")

    with col3:
        animated_kpi("Médecins pour 1000 hab.", "3.8", "2024")

    with col4:
        animated_kpi("Taux d'obésité adulte", "17 %", "estimation 2025")

    st.markdown("</div>", unsafe_allow_html=True)

    # Graphique placeholder (à remplacer dès que tu as un CSV santé)
    st.info("Aucun fichier CSV santé fourni pour l'instant. Voici un exemple de visualisation.")
    data_placeholder = pd.DataFrame({
        "Année": [2019, 2020, 2021, 2022, 2023],
        "Taux d'hospitalisation (pour 1000 hab.)": [120, 185, 160, 140, 130],
        "Consultations médicales par habitant": [5.2, 4.8, 5.0, 5.1, 5.3]
    })
    fig = px.line(data_placeholder, x="Année", y=["Taux d'hospitalisation (pour 1000 hab.)", "Consultations médicales par habitant"],
                  title="Indicateurs santé (données fictives en attente de CSV réel)")
    fig.update_layout(legend_title_text="Indicateur")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="margin-top:40px; padding:20px; background:rgba(30,41,59,0.5); border-radius:16px;">
        <h4>Prochaines étapes pour la page Santé</h4>
        <ul>
            <li>Espérance de vie par commune</li>
            <li>Prévalence maladies chroniques (diabète, hypertension, cancers)</li>
            <li>Accès aux soins (densité médecins, délais RDV)</li>
            <li>Taux de couverture vaccinale</li>
        </ul>
        <p>Envoie-moi le fichier CSV santé quand tu l'as (ex: santé.csv, morbidité.csv, etc.) et je l'intègre en 2 minutes.</p>
    </div>
    """, unsafe_allow_html=True)
