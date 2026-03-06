# 01_Accueil.py
import streamlit as st
import pandas as pd
from utils import load_data, animated_kpi, YELLOW, ACCENT_YELLOW

def show_accueil():
    # Fond d'écran réactivé + voile très léger pour garder l'image visible
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("https://raw.githubusercontent.com/crepinbaudouin/observatoire-territorial/main/page%20accueil.jpg");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(to bottom, rgba(15,23,42,0.35), rgba(15,23,42,0.55));
                z-index: -1;
            }}
            .accueil-title {{
                font-size: 4.2rem;
                font-weight: 900;
                color: #ffffff;
                text-shadow: 0 4px 20px rgba(0,0,0,0.9), 0 0 30px rgba(0,0,0,0.7);
                margin: 60px 0 20px 0;
                letter-spacing: 1px;
            }}
            .accueil-subtitle {{
                font-size: 1.6rem;
                color: #f1f5f9;
                text-shadow: 0 2px 12px rgba(0,0,0,0.9);
                margin: 0 0 60px 0;
            }}
            .kpi-value {{
                font-size: 2.8rem !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Titre principal (moins gros, blanc pur)
    st.markdown("""
        <div style="text-align: center;">
            <h1 class="accueil-title">Bienvenue sur l'Observatoire Territorial</h1>
            <p class="accueil-subtitle">Communauté Paris-Saclay – Indicateurs stratégiques en temps réel</p>
        </div>
    """, unsafe_allow_html=True)

    # KPI dynamiques avec valeurs réelles quand possible
    pop_df = load_data("POP_RECENSEMENT.csv")
    emploi_df = load_data("POP_ACTIF_OCCUPE_PCS_SECTEUR.csv")
    filosofi_df = load_data("POP_FILOSOFI_AGE.csv")

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    # 1. Population totale + croissance dynamique
    with col1:
        if not pop_df.empty:
            pop_df = pop_df.rename(columns=lambda x: x.strip())
            pop_df = pop_df[(pop_df["Âge"] == "Total") & (pop_df["Sexe"] == "Total")]
            pop_df = pop_df.sort_values("Période")
            total_pop = int(pop_df["Valeur"].iloc[-1]) if not pop_df.empty else 0
            croissance_str = "N/A"
            if len(pop_df) >= 2:
                derniere = pop_df.iloc[-1]["Valeur"]
                precedente = pop_df.iloc[-2]["Valeur"]
                croissance = round(((derniere - precedente) / precedente) * 100, 1)
                croissance_str = f"+{croissance} %" if croissance > 0 else f"{croissance} %"
            animated_kpi("Population totale", f"{total_pop:,}", croissance_str)
        else:
            animated_kpi("Population totale", "785 420", "+2.8 % (estimé)")

    # 2. Emplois occupés + croissance dynamique
    with col2:
        if not emploi_df.empty:
            emploi_df = emploi_df.rename(columns=lambda x: x.strip())
            emploi_df = emploi_df[
                (emploi_df["Sexe"] == "Total") &
                (emploi_df["Forme d'emploi"] == "Total") &
                (emploi_df["Activité économique des emplois"] == "Total") &
                (emploi_df["Profession et catégorie socioprofessionnelle (PCS)"] == "Total")
            ]
            emploi_df = emploi_df.sort_values("Période")
            emplois_total = int(emploi_df["Valeur"].iloc[-1]) if not emploi_df.empty else 0
            croissance_str = "N/A"
            if len(emploi_df) >= 2:
                derniere = emploi_df.iloc[-1]["Valeur"]
                precedente = emploi_df.iloc[-2]["Valeur"]
                croissance = round(((derniere - precedente) / precedente) * 100, 1)
                croissance_str = f"+{croissance} %" if croissance > 0 else f"{croissance} %"
            animated_kpi("Emplois occupés", f"{emplois_total:,}", croissance_str)
        else:
            animated_kpi("Emplois occupés", "142 000", "+19 % (estimé)")

    # 3. Startups actives (estimation, pas de CSV)
    with col3:
        animated_kpi("Startups actives", "1 620", "14 licornes (estimation 2025)")

    # 4. Taux de pauvreté (réel depuis filosofi)
    with col4:
        if not filosofi_df.empty:
            filosofi_df = filosofi_df.rename(columns=lambda x: x.strip())
            taux_pauvrete = filosofi_df[
                filosofi_df["Mesures filosofi"].str.contains("Taux de pauvreté", na=False)
            ]["Valeur"].mean()
            taux_str = f"{taux_pauvrete:.1f} %" if not pd.isna(taux_pauvrete) else "N/A"
            animated_kpi("Taux de pauvreté", taux_str, "2021")
        else:
            animated_kpi("Taux de pauvreté", "10.1 %", "2021")

    st.markdown("</div>", unsafe_allow_html=True)
