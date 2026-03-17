import streamlit as st
import pandas as pd
import random
import time
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Bus Simulator Online", page_icon="🚌", layout="wide")

# Fichier pour sauvegarder les scores
SCORE_FILE = "scores_bus.csv"

def charger_scores():
    if os.path.exists(SCORE_FILE):
        return pd.read_csv(SCORE_FILE)
    return pd.DataFrame(columns=["Pseudo", "XP"])

def sauvegarder_score(pseudo, xp):
    df = charger_scores()
    if pseudo in df["Pseudo"].values:
        df.loc[df["Pseudo"] == pseudo, "XP"] += xp
    else:
        new_row = pd.DataFrame({"Pseudo": [pseudo], "XP": [xp]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(SCORE_FILE, index=False)

# --- INITIALISATION ---
if 'xp_session' not in st.session_state:
    st.session_state.xp_session = 0
if 'en_service' not in st.session_state:
    st.session_state.en_service = False

# --- BARRE LATÉRALE : PROFIL ---
st.sidebar.title("🎮 Espace Chauffeur")
pseudo = st.sidebar.text_input("Ton Pseudo :", value="Chauffeur_Anonyme")
st.sidebar.metric("XP Gagnée ce jour", st.session_state.xp_session)

# Affichage du Leaderboard
st.sidebar.subheader("🏆 Classement Online")
df_scores = charger_scores().sort_values(by="XP", ascending=False).head(5)
st.sidebar.table(df_scores)

# --- INTERFACE PRINCIPALE ---
st.title("🚌 Bus Simulator Online")
st.markdown("---")

# 1. Choix du Bus et de la Ligne
if not st.session_state.en_service:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚐 Choisir ton bus")
        bus_type = st.radio("Modèle :", ["Minibus (Rapide)", "Bus Standard (Équilibré)", "Bus Articulé (Difficile)"])
    
    with col2:
        st.subheader("🗺️ Choisir ta ligne")
        lignes = {
            "Altkirch - Ferrette (829)": {"distance": 20, "gain": 40},
            "Altkirch - Mulhouse (821)": {"distance": 35, "gain": 80},
            "Navette Sundgauvienne": {"distance": 10, "gain": 20}
        }
        ligne_choisie = st.selectbox("Destination :", list(lignes.keys()))

    if st.button("🚀 Démarrer le Service"):
        st.session_state.en_service = True
        st.session_state.ligne_actuelle = ligne_choisie
        st.session_state.info_ligne = lignes[ligne_choisie]
        st.rerun()

# 2. Simulation du Trajet
else:
    st.header(f"📍 Trajet en cours : {st.session_state.ligne_actuelle}")
    
    # Barre de progression
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulation d'événements aléatoires
    evenements = [
        "Tout est calme, les passagers admirent le Sundgau. 🌲",
        "Attention ! Un tracteur bloque la route près d'Hirsingue. 🚜",
        "Arrêt demandé ! Un passager monte à bord. 🚏",
        "Pluie battante, ralentissez pour la sécurité ! 🌧️"
    ]
    
    for i in range(1, 101):
        time.sleep(0.05) # On simule le trajet
        progress_bar.progress(i)
        if i % 25 == 0:
            status_text.info(random.choice(evenements))
            
    # Fin de trajet
    st.success(f"🏁 Terminus ! Vous avez atteint votre destination.")
    xp_gagne = st.session_state.info_ligne["gain"]
    
    if st.button("💰 Encaisser l'XP et Terminer"):
        st.session_state.xp_session += xp_gagne
        sauvegarder_score(pseudo, xp_gagne)
        st.session_state.en_service = False
        st.rerun()

# --- BAS DE PAGE ---
st.markdown("---")
st.caption("Projet : Bus Simulator Online - Développé en Python avec Streamlit")
