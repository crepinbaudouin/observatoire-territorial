# 09_Finance.py
import streamlit as st
from utils import YELLOW

def show_finance():
    st.title("Finance (restreint)")

    if "finance_open" not in st.session_state:
        st.session_state.finance_open = False

    if st.button("Accéder à Finance", type="primary"):
        st.session_state.finance_open = True

    if st.session_state.finance_open:
        st.markdown(f"""
        <div class="modal">
            <div class="modal-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="color:{YELLOW}; margin: 0;">Finance</h2>
                    <button style="
                        background: none;
                        border: none;
                        font-size: 1.8rem;
                        color: #94a3b8;
                        cursor: pointer;
                    " onclick="parent.document.querySelector('iframe').contentWindow.postMessage('close_modal', '*')">✕</button>
                </div>
                <input class="login-input" placeholder="Identifiant" type="text">
                <input class="login-input" placeholder="Mot de passe" type="password">
                <button class="login-btn">Se connecter</button>
                <p style="text-align:center; margin-top:20px; color:#94a3b8;">
                    <a href="#" style="color:{YELLOW};">Mot de passe oublié ?</a>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Fermer la fenêtre"):
            st.session_state.finance_open = False
            st.rerun()
