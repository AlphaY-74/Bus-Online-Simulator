import streamlit as st
import pandas as pd
import time
import random

# --- CONFIGURATION VISUELLE ---
st.set_page_config(page_title="BUS SIMULATOR ONLINE", layout="wide", page_icon="🚌")

# Injection de CSS pour un look "Gaming"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff2b2b; transform: scale(1.02); }
    .status-box {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #3e3e3e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES ET LOGIQUE ---
if 'carburant' not in st.session_state:
    st.session_state.carburant = 100
    st.session_state.argent = 500
    st.session_state.messages = ["Système : Bienvenue chauffeur !"]

# --- SIDEBAR (Le Profil) ---
with st.sidebar:
    st.image("https://img.freepik.com/vecteurs-premium/logo-bus-vectoriel-concept-conception-logo-transport-bus-illustration-vectorielle-isolee_636060-496.jpg", width=100)
    st.title("🕹️ Cockpit")
    st.metric("Portefeuille", f"{st.session_state.argent} €")
    st.write(f"⛽ Carburant : {'🔴' if st.session_state.carburant < 20 else '🟢'} {st.session_state.carburant}%")
    st.progress(st.session_state.carburant / 100)
    
    st.markdown("---")
    st.subheader("💬 Chat Online")
    for msg in st.session_state.messages[-5:]:
        st.caption(msg)
    chat_input = st.text_input("Envoyer un message :", key="chat")
    if st.button("Envoyer"):
        st.session_state.messages.append(f"Moi : {chat_input}")
        st.rerun()

# --- CORPS DU JEU ---
col_stats, col_jeu = st.columns([1, 2])

with col_stats:
    st.subheader("🚐 Ton Véhicule")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Iveco_Crossway_LE_R%C3%A9seau_67.jpg/1200px-Iveco_Crossway_LE_R%C3%A9seau_67.jpg", caption="Iveco Crossway - Edition Sundgau")
    
    if st.button("⛽ Faire le plein (50€)"):
        if st.session_state.argent >= 50:
            st.session_state.argent -= 50
            st.session_state.carburant = 100
            st.success("Réservoir plein !")
            st.rerun()

with col_jeu:
    st.subheader("🛣️ Prochaine Tournée")
    
    ligne = st.selectbox("Ligne active :", ["Ligne 829 : Altkirch > Ferrette", "Ligne 821 : Mulhouse Express", "Navette de Nuit"])
    
    if st.button("🏁 DÉMARRER LE SERVICE"):
        if st.session_state.carburant > 20:
            # Animation de conduite
            with st.status("🚌 Bus en circulation dans le Sundgau...", expanded=True) as status:
                st.write("Passage à Hirsingue...")
                time.sleep(1)
                st.write("Arrêt à la gare d'Altkirch...")
                time.sleep(1)
                st.write("Montée des passagers lycéens...")
                time.sleep(1)
                status.update(label="Course terminée !", state="complete", expanded=False)
            
            # Résultats
            gain = random.randint(80, 150)
            st.session_state.argent += gain
            st.session_state.carburant -= 15
            st.balloons()
            st.success(f"Bravo ! Tu as encaissé {gain}€.")
            st.session_state.messages.append(f"Système : Course terminée sur la {ligne} !")
        else:
            st.error("Pas assez de carburant pour partir !")

# --- SYSTÈME DE CARTES (Le bonus attirant) ---
st.markdown("---")
st.subheader("📍 Carte du Réseau en Temps Réel")
# Création d'une fausse position de bus aléatoire
bus_pos = pd.DataFrame({
    'lat': [47.62 + random.uniform(-0.05, 0.05)],
    'lon': [7.23 + random.uniform(-0.05, 0.05)]
})
st.map(bus_pos)
