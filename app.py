import streamlit as st

# Barre fixe en haut
st.markdown("""
    <style>
        .topbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 999;
        }
        .logo-title {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .nav-links {
            display: flex;
            gap: 30px;
        }
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: color 0.3s;
        }
        .nav-links a:hover, .nav-links a.active {
            color: #FDD100;
        }
        .finance-btn {
            background: #6A1B9A;
            color: white;
            padding: 10px 24px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
        }
        .finance-btn:hover {
            background: #9F7AEA;
        }
        .main-content {
            margin-top: 100px;
            padding: 20px 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Contenu barre fixe
st.markdown("""
    <div class="topbar">
        <div class="logo-title">
            <img src="logo_paris_saclay.png" width="60">
            <div>
                <h2 style="margin:0; color:#000;">PARIS <span style="color:#FDD100;">●</span> SACLAY</h2>
                <small style="color:#555;">Communauté d'agglomération</small>
            </div>
        </div>

        <div class="nav-links">
            <a href="#" class="active">Accueil</a>
            <a href="#">Population</a>
            <a href="#">Emploi / Chômage</a>
            <a href="#">Économie</a>
            <a href="#">Social / Ménages</a>
            <a href="#">Santé</a>
            <a href="#">Éducation</a>
            <a href="#">Sports</a>
        </div>

        <a href="#" class="finance-btn">Finance (restreint)</a>
    </div>

    <div class="main-content">
        <!-- Ici ton contenu principal -->
        <h1>Bienvenue sur l'Observatoire</h1>
        <p>Le contenu change selon la page sélectionnée...</p>
    </div>
""", unsafe_allow_html=True)
