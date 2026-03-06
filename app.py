# app.py
import streamlit as st
from utils import load_data, animated_kpi, get_theme_css

st.set_page_config(
    page_title="Observatoire Territorial Paris-Saclay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Toggle dark/light (commun à toutes les pages)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark_light = st.toggle("Dark / Light", value=st.session_state.dark_mode)
if dark_light != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_light
    st.rerun()

# Appliquer CSS global
st.markdown(f"<style>{get_theme_css()}</style>", unsafe_allow_html=True)

# Barre haute commune
col_logo, col_title, col_toggle = st.columns([1, 5, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=70)

with col_title:
    st.markdown("""
        <h1 style="margin:0; text-align:center; font-size:2.6rem;">
            PARIS <span style="color:#FDD100;">●</span> SACLAY
        </h1>
        <p style="text-align:center; color:#94a3b8; margin:4px 0 0;">
            Communauté d'agglomération
        </p>
    """, unsafe_allow_html=True)

# Navigation horizontale (radio personnalisé)
themes = [
    "Accueil", "Population", "Emploi / Chômage", "Économie",
    "Social / Ménages", "Santé", "Éducation", "Sports", "Finance"
]

selected = st.radio(
    "Navigation",
    themes,
    horizontal=True,
    label_visibility="collapsed"
)

# Import et exécution de la page sélectionnée
if selected == "Accueil":
    from Accueil import show_accueil
    show_accueil()
elif selected == "Population":
    from Population import show_population
    show_population()
elif selected == "Emploi / Chômage":
    from Emploi_Chômage import show_emploi_chomage
    show_emploi_chomage()
elif selected == "Économie":
    from Économie import show_economie
    show_economie()
elif selected == "Social / Ménages":
    from Social_Ménages import show_social_menages
    show_social_menages()
elif selected == "Santé":
    from Santé import show_sante
    show_sante()
elif selected == "Éducation":
    from Éducation import show_education
    show_education()
elif selected == "Sports":
    from Sports import show_sports
    show_sports()
elif selected == "Finance":
    from Finance import show_finance
    show_finance()
