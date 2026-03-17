import streamlit as st
import random

st.set_page_config(page_title="Express Sundgoviens", page_icon="🚌")
st.title("🚌 Express Sundgoviens : Le Jeu")

# Initialisation de l'état du jeu
if 'argent' not in st.session_state:
    st.session_state.argent = 100
    st.session_state.carburant = 100
    st.session_state.etape = "Dépôt d'Altkirch"

# Interface de bord
col1, col2, col3 = st.columns(3)
col1.metric("Argent", f"{st.session_state.argent}€")
col2.metric("Carburant", f"{st.session_state.carburant}%")
col3.info(f"Lieu actuel : {st.session_state.etape}")

# Actions
st.subheader("Prochaine destination")
destinations = {
    "Ferrette": {"distance": 15, "gain": 50},
    "Dannemarie": {"distance": 20, "gain": 70},
    "Hirsingue": {"distance": 5, "gain": 20}
}

for ville, info in destinations.items():
    if st.button(f"Aller à {ville} (+{info['gain']}€)"):
        # Logique de déplacement
        st.session_state.carburant -= info['distance']
        st.session_state.argent += info['gain']
        st.session_state.etape = ville
        
        # Événement aléatoire
        if random.random() < 0.3:
            st.warning("⚠️ Embouteillage à la sortie d'Altkirch ! Perte de carburant supplémentaire.")
            st.session_state.carburant -= 5
        
        st.rerun()

# Fin de partie
if st.session_state.carburant <= 0:
    st.error("Panne sèche ! Partie terminée.")
    if st.button("Recommencer"):
        st.session_state.clear()
        st.rerun()
