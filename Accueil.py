# 01_Accueil.py
import streamlit as st
from utils import load_data, animated_kpi

def show_accueil():
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 100px 20px 60px;
            background: linear-gradient(to bottom, rgba(15,23,42,0.45), rgba(15,23,42,0.65));
            border-radius: 0 0 40px 40px;
            margin: 0 -40px 40px -40px;
        ">
            <h1 style="
                font-size: 5.2rem;
                font-weight: 900;
                margin: 0 0 20px 0;
                color: #ffffff;
                text-shadow: 0 0 25px rgba(0,0,0,0.95), 0 0 50px rgba(0,0,0,0.8), 0 6px 30px rgba(0,0,0,0.7);
                letter-spacing: 1px;
            ">
                Bienvenue sur l'Observatoire Territorial
            </h1>
            <p style="
                font-size: 1.9rem;
                color: #f1f5f9;
                margin: 0;
                text-shadow: 0 3px 15px rgba(0,0,0,0.9);
            ">
                Communauté Paris-Saclay – Indicateurs stratégiques en temps réel
            </p>
        </div>
    """, unsafe_allow_html=True)

    pop_df = load_data("POP_RECENSEMENT.csv")
    emploi_df = load_data("POP_ACTIF_OCCUPE_PCS_SECTEUR.csv")
    filosofi_df = load_data("POP_FILOSOFI_AGE.csv")

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

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
            animated_kpi("Population totale", "N/A", "données manquantes")

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
            animated_kpi("Emplois occupés", "N/A", "données manquantes")

    with col3:
        animated_kpi("Startups actives", "1 620", "14 licornes (estimation)")

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
