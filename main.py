import streamlit as st
import pandas as pd
import os

DB_REGIONS = "regions_communaute.csv"

# --- FONCTIONS DE GESTION ---
def charger_regions():
    if os.path.exists(DB_REGIONS):
        return pd.read_csv(DB_REGIONS)
    # Régions par défaut si le fichier n'existe pas
    return pd.DataFrame([
        {"Nom": "Sundgau Central", "Gain": 100, "Statut": "publié", "Auteur": "Admin"},
        {"Nom": "Vallée de la Doller", "Gain": 120, "Statut": "publié", "Auteur": "Admin"}
    ])

def ajouter_proposition(nom, gain, auteur):
    df = charger_regions()
    # On vérifie si elle n'existe pas déjà
    if nom not in df["Nom"].values:
        nouvelle_region = pd.DataFrame([{"Nom": nom, "Gain": gain, "Statut": "en_attente", "Auteur": auteur}])
        df = pd.concat([df, nouvelle_region], ignore_index=True)
        df.to_csv(DB_REGIONS, index=False)
        return True
    return False

def valider_region(nom, action):
    df = charger_regions()
    if action == "publier":
        df.loc[df["Nom"] == nom, "Statut"] = "publié"
    elif action == "supprimer":
        df = df[df["Nom"] != nom]
    df.to_csv(DB_REGIONS, index=False)

# --- INTERFACE ---
st.title("🗺️ Extension du Réseau")

menu = ["Jouer", "Proposer une Région", "🛡️ Admin"]
choix = st.sidebar.selectbox("Menu Navigation", menu)

# --- SECTION 1 : JOUER (Affiche seulement le 'publié') ---
if choix == "Jouer":
    st.header("Choisir une destination validée")
    df = charger_regions()
    regions_dispos = df[df["Statut"] == "publié"]
    
    for index, row in regions_dispos.iterrows():
        with st.expander(f"📍 {row['Nom']}"):
            st.write(f"Gain estimé : {row['Gain']} €")
            st.caption(f"Ajouté par : {row['Auteur']}")
            if st.button(f"Conduire vers {row['Nom']}", key=index):
                st.info(f"Départ imminent pour {row['Nom']} !")

# --- SECTION 2 : PROPOSER ---
elif choix == "Proposer une Région":
    st.header("Suggérer une nouvelle zone de jeu")
    with st.form("form_region"):
        nom_p = st.text_input("Nom de la région (ex: Alsace Bossue, Jura...)")
        gain_p = st.number_input("Gain par course (€)", min_value=10, max_value=1000, value=100)
        auteur_p = st.text_input("Ton pseudo")
        submit = st.form_submit_button("Envoyer pour validation")
        
        if submit:
            if nom_p and auteur_p:
                if ajouter_proposition(nom_p, gain_p, auteur_p):
                    st.success("✅ Proposition envoyée ! Un admin va l'étudier.")
                else:
                    st.warning("Cette région est déjà dans la liste.")
            else:
                st.error("Remplis tous les champs !")

# --- SECTION 3 : ADMIN (Protégé par mot de passe) ---
elif choix == "🛡️ Admin":
    st.header("Panneau de modération")
    password = st.text_input("Code secret Admin", type="password")
    
    if password == "sundgau2026": # Ton mot de passe
        df = charger_regions()
        en_attente = df[df["Statut"] == "en_attente"]
        
        if en_attente.empty:
            st.write("Aucune proposition en attente. ☕")
        else:
            for index, row in en_attente.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**{row['Nom']}** (par {row['Auteur']}) - {row['Gain']}€")
                if col2.button("✅ Publier", key=f"pub{index}"):
                    valider_region(row['Nom'], "publier")
                    st.rerun()
                if col3.button("❌ Refuser", key=f"ref{index}"):
                    valider_region(row['Nom'], "supprimer")
                    st.rerun()
    elif password:
        st.error("Code incorrect !")
