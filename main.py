import streamlit as st
import pandas as pd
import random
import time
import os

# --- CONFIGURATION ET STYLE ---
st.set_page_config(page_title="Bus Simulator Online", page_icon="🚌", layout="wide")

# Simulation d'une base de données locale
DB_FILE = "bus_sim_data.csv"

def charger_donnees():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Pseudo", "XP", "Argent"])

def sauvegarder_donnees(pseudo, xp, argent):
    df = charger_donnees()
    if pseudo in df["Pseudo"].values:
        df.loc[df["Pseudo"] == pseudo, "XP"] += xp
        df.loc[df["Pseudo"] == pseudo, "Argent"] += argent
    else:
        new_row = pd.DataFrame({"Pseudo": [pseudo], "XP": [xp], "Argent": [argent]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- INITIALISATION SESSION ---
if 'argent' not in st.session_state:
    st.session_state.argent = 500  # Budget de départ
    st.session_state.bus_possedes = ["Minibus Occasion"]
    st.session_state.bus_actuel = "Minibus Occasion"
    st.session_state.en_service = False

# --- SIDEBAR : TABLEAU DE BORD ---
st.sidebar.title("🎮 Dashboard Chauffeur")
pseudo = st.sidebar.text_input("Ton Pseudo :", value="Chauffeur_Anonyme")

# Récupérer les données globales
stats_globales = charger_donnees()
ma_ligne = stats_globales[stats_globales["Pseudo"] == pseudo]
xp_totale = ma_ligne["XP"].values[0] if not ma_ligne.empty else 0
argent_total = ma_ligne["Argent"].values[0] if not ma_ligne.empty else st.session_state.argent

st.sidebar.metric("💰 Portefeuille", f"{argent_total} €")
st.sidebar.metric("⭐ Expérience", f"{xp_totale} XP")

st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Top 3 Mondiaux")
st.sidebar.table(stats_globales.sort_values("XP", ascending=False).head(3)[["Pseudo", "XP"]])

# --- INTERFACE PRINCIPALE ---
tab1, tab2, tab3 = st.tabs(["🚀 Service", "🏗️ Garage", "🗺️ Carte du Réseau"])

# --- TAB 1 : LE SERVICE ---
with tab1:
    if not st.session_state.en_service:
        st.header("Prêt pour le départ ?")
        
        lignes = {
            "Altkirch ↔ Ferrette": {"coordonnees": [47.623, 7.239], "gain": 150, "xp": 40},
            "Dannemarie ↔ Altkirch": {"coordonnees": [47.611, 7.117], "gain": 200, "xp": 60},
            "Hirsingue ↔ Waldighofen": {"coordonnees": [47.584, 7.251], "gain": 120, "xp": 30}
        }
        
        col1, col2 = st.columns(2)
        with col1:
            choix_ligne = st.selectbox("Choisir une ligne :", list(lignes.keys()))
            meteo = random.choice(["Ensoleillé ☀️", "Pluie 🌧️", "Brouillard 🌫️"])
            st.write(f"Météo actuelle : **{meteo}**")
        
        with col2:
            st.write(f"Bus utilisé : **{st.session_state.bus_actuel}**")
            multiplier = 1.5 if meteo != "Ensoleillé ☀️" else 1.0
            st.write(f"Prime météo : x{multiplier}")

        if st.button("Démarrer la tournée"):
            st.session_state.en_service = True
            st.session_state.ligne_active = choix_ligne
            st.session_state.gain_potentiel = int(lignes[choix_ligne]["gain"] * multiplier)
            st.session_state.xp_potentielle = lignes[choix_ligne]["xp"]
            st.rerun()
    else:
        st.header(f"🚏 En route vers {st.session_state.ligne_active}")
        progress = st.progress(0)
        status = st.empty()
        
        for i in range(101):
            time.sleep(0.04)
            progress.progress(i)
            if i == 20: status.warning("Passagers bruyants à l'arrière... 📢")
            if i == 50: status.info("Check-point : Altkirch Centre. ✅")
            if i == 80: status.success("Le terminus approche ! 🏁")
        
        if st.button("Terminer et encaisser"):
            sauvegarder_donnees(pseudo, st.session_state.xp_potentielle, st.session_state.gain_potentiel)
            st.session_state.en_service = False
            st.success(f"Bravo ! +{st.session_state.gain_potentiel}€ et +{st.session_state.xp_potentielle}XP")
            st.rerun()

# --- TAB 2 : LE GARAGE ---
with tab2:
    st.header("Acheter un nouveau bus")
    catalogue = {
        "Bus Standard Fluo": 1500,
        "Autocar de Grand Tourisme": 5000,
        "Bus Électrique Sundgau": 12000
    }
    
    for bus, prix in catalogue.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{bus}** - {prix} €")
        if bus in st.session_state.bus_possedes:
            c2.success("Possédé")
            if st.session_state.bus_actuel != bus:
                if c2.button("Choisir", key=bus):
                    st.session_state.bus_actuel = bus
                    st.rerun()
        else:
            if c2.button("Acheter", key=bus):
                if argent_total >= prix:
                    sauvegarder_donnees(pseudo, 0, -prix) # On déduit l'argent
                    st.session_state.bus_possedes.append(bus)
                    st.success(f"Félicitations ! Tu as acheté le {bus}")
                    st.rerun()
                else:
                    st.error("Fonds insuffisants !")

# --- TAB 3 : CARTE DU RÉSEAU ---
with tab3:
    st.header("Carte des lignes du Sundgau")
    # Coordonnées réelles approximatives du Sundgau
    map_data = pd.DataFrame({
        'lat': [47.6231, 47.6115, 47.5847, 47.4893],
        'lon': [7.2392, 7.1171, 7.2514, 7.3117]
    })
    st.map(map_data)
    st.caption("Points desservis : Altkirch, Dannemarie, Hirsingue, Ferrette.")
