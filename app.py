import streamlit as st

# Menu horizontal avec radio stylé
st.markdown("""
    <style>
        .stRadio > div > label {
            background: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .stRadio > div > label:hover {
            background: #FDD100;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

col_logo, col_menu, col_finance = st.columns([1, 6, 1])

with col_logo:
    st.image("logo_paris_saclay.png", width=80)

with col_menu:
    theme = st.radio(
        "Thématiques",
        ["Accueil", "Population", "Emploi", "Économie", "Social", "Santé", "Éducation", "Sports"],
        horizontal=True,
        key="theme_menu"
    )

with col_finance:
    if st.button("Finance (restreint)", type="primary"):
        st.session_state["finance_open"] = True

# Modal Finance
if "finance_open" in st.session_state and st.session_state["finance_open"]:
    with st.expander("Accès Finance", expanded=True):
        st.text_input("Identifiant")
        st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            st.success("Connexion en cours...")
