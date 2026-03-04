import streamlit as st

# Logo + titre en haut (comme ta maquette)
col_logo, col_titre = st.columns([1, 5])
with col_logo:
    st.image("logo_paris_saclay.png", width=120)

with col_titre:
    st.markdown("""
    <h1 style="margin:0; color:#000; font-weight:bold;">
        PARIS <span style="color:#FDD100;">●</span> SACLAY
    </h1>
    <p style="margin:0; color:#333; font-size:1.1rem;">
        Communauté d'agglomération
    </p>
    """, unsafe_allow_html=True)

# Barre de menu horizontale (tabs)
tabs = st.tabs([
    "Accueil",
    "Population",
    "Emploi / Chômage",
    "Économie",
    "Social / Ménages",
    "Santé",
    "Éducation",
    "Sports",
    "Finance (restreint)"
])

# Contenu selon onglet actif
if tabs[0].active:
    st.write("Contenu Accueil")
elif tabs[1].active:
    st.write("Contenu Population")
# ... etc.
