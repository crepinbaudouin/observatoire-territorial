# app.py - Observatoire Territorial Paris-Saclay - Style maquette 2026
import streamlit as st
from streamlit.components.v1 import html
import base64

# Config
st.set_page_config(page_title="Observatoire Territorial Paris-Saclay", layout="wide", initial_sidebar_state="collapsed")

# Fond d'écran
fond_path = "page accueil.jpg"  # ou URL si hébergé
with open(fond_path, "rb") as f:
    fond_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{fond_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.45), rgba(0,0,0,0.65));
            z-index: -2;
        }}
        /* Bandeau navigation horizontal */
        .nav-bar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255,255,255,0.12);
            padding: 12px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 999;
        }}
        .nav-links {{
            display: flex;
            gap: 32px;
        }}
        .nav-links a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }}
        .nav-links a:hover {{
            color: #FDD100;
            text-shadow: 0 0 12px #FDD10080;
        }}
        .finance-btn {{
            background: linear-gradient(45deg, #6A1B9A, #9F7AEA);
            color: white;
            padding: 10px 28px;
            border-radius: 50px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(106,27,154,0.4);
            transition: all 0.3s;
        }}
        .finance-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(106,27,154,0.6);
        }}
        /* Hero central */
        .hero {{
            height: 85vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            padding: 0 10%;
        }}
        .hero h1 {{
            font-size: 5.8rem;
            margin: 0;
            background: linear-gradient(90deg, #FDD100, #9F7AEA, #FDD100);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientFlow 12s ease infinite;
        }}
        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 200% 50%; }}
        }}
        .hero .play-btn {{
            margin-top: 40px;
            width: 120px;
            height: 120px;
            background: rgba(253,209,0,0.25);
            border: 3px solid #FDD100;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            color: white;
            cursor: pointer;
            transition: all 0.4s;
        }}
        .hero .play-btn:hover {{
            background: rgba(253,209,0,0.45);
            transform: scale(1.15);
        }}
        /* Login modal Finance */
        .finance-modal {{
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}
        .modal-content {{
            background: rgba(26,31,46,0.95);
            backdrop-filter: blur(16px);
            border: 1px solid #6A1B9A;
            border-radius: 20px;
            padding: 40px;
            width: 420px;
            text-align: center;
            color: white;
        }}
        .modal-content input {{
            width: 100%;
            padding: 14px;
            margin: 12px 0;
            border-radius: 8px;
            border: 1px solid #6A1B9A;
            background: rgba(255,255,255,0.08);
            color: white;
        }}
        .modal-content button {{
            background: linear-gradient(45deg, #6A1B9A, #9F7AEA);
            color: white;
            padding: 14px 40px;
            border: none;
            border-radius: 50px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# ─── Bandeau navigation horizontal ──────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div style="font-size:1.6rem; font-weight:bold; color:#FDD100;">
        Observatoire Paris-Saclay
    </div>
    <div class="nav-links">
        <a href="#">Population</a>
        <a href="#">Emploi / Chômage</a>
        <a href="#">Économie</a>
        <a href="#">Social / Ménages</a>
        <a href="#">Santé</a>
        <a href="#">Éducation</a>
        <a href="#">Sports</a>
    </div>
    <button class="finance-btn" onclick="document.getElementById('finance-modal').style.display='flex'">
        Finance
    </button>
</div>
""", unsafe_allow_html=True)

# ─── Hero central ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <h1>Observatoire Territorial</h1>
        <p style="font-size:1.8rem; margin:2rem 0; color:#E0E0E0;">
            Suivi stratégique en temps réel – Agglomération Paris-Saclay
        </p>
        <div class="play-btn">▶</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Modal Finance ──────────────────────────────────────────────────────────────
st.markdown("""
<div id="finance-modal" class="finance-modal" style="display:none;">
    <div class="modal-content">
        <h2 style="color:#FDD100;">Accès Finance</h2>
        <input type="text" placeholder="Identifiant">
        <input type="password" placeholder="Mot de passe">
        <button>Se connecter</button>
        <p style="margin-top:20px; font-size:0.9rem; color:#aaa;">
            © 2023 Taipy | Mentions légales | Politique de confidentialité
        </p>
    </div>
</div>

<script>
    document.addEventListener('click', function(e) {
        if (e.target.id === 'finance-modal' || e.target.closest('.modal-content') === null) {
            document.getElementById('finance-modal').style.display = 'none';
        }
    });
</script>
""", unsafe_allow_html=True)

# ─── Contenu principal (exemple) ────────────────────────────────────────────────
st.title("Bienvenue")
st.write("Sélectionnez une thématique dans la barre de navigation ci-dessus.")

# KPI exemple
st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    st.markdown(f"""
    <div class="kpi-hex" style="border-color:{YELLOW};">
        <h3 style="color:{YELLOW};">Population</h3>
        <div class="kpi-number" style="color:{YELLOW};">785 420</div>
    </div>
    """, unsafe_allow_html=True)
# ... ajoute les autres KPI ici

st.markdown("</div>", unsafe_allow_html=True)
