import streamlit as st
import pandas as pd
from datetime import date
import time

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sport", page_icon="🏋️")

st.title("🏋️ Mon Suivi de Sport")

# Initialisation de la base de données locale (session_state)
if "exercices" not in st.session_state:
    st.session_state.exercices = [
        {"nom": "Pompes", "type": "Répétitions"},
        {"nom": "Gainage", "type": "Chrono (sec)"}
    ]

if "historique" not in st.session_state:
    st.session_state.historique = []

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🏋️ Entraînement", "➕ Créer Exercice", "📊 Historique"])

# --- 1. S'ENTRAÎNER ---
with tab1:
    st.header("Nouvelle séance")
    
    if not st.session_state.exercices:
        st.warning("Commence par créer un exercice dans l'onglet dédié !")
    else:
        # Sélection des exercices pour la séance
        noms_ex = [ex["nom"] for ex in st.session_state.exercices]
        ex_selectionnes = st.multiselect("Choisis les exercices de la séance :", noms_ex, default=noms_ex)
        
        form_data = {}
        
        for nom in ex_selectionnes:
            ex_obj = next(item for item in st.session_state.exercices if item["nom"] == nom)
            st.subheader(f"👉 {nom}")
            
            nb_series = st.number_input(f"Nombre de séries pour {nom}", min_value=1, max_value=10, value=3, key=f"series_{nom}")
            
            # Gestion du chrono interactif si c'est du gainage / temps
            if "Chrono" in ex_obj["type"]:
                durée = st.number_input(f"Objectif par série (secondes) :", min_value=5, value=30, step=5, key=f"target_{nom}")
                if st.button(f"⏱️ Lancer le chrono ({durée}s)", key=f"btn_{nom}"):
                    progress_bar = st.progress(0)
                    for t in range(durée):
                        time.sleep(1)
                        progress_bar.progress((t + 1) / durée)
                    st.success("Terminé ! 🔥")
                
                form_data[nom] = f"{nb_series} séries de {durée}s"
            else:
                reps = st.number_input(f"Répétitions par série :", min_value=1, value=10, key=f"reps_{nom}")
                form_data[nom] = f"{nb_series} séries de {reps} reps"

        if st.button("✅ Valider et enregistrer la séance", type="primary"):
            date_du_jour = date.today().strftime("%d/%m/%Y")
            for ex_nom, details in form_data.items():
                st.session_state.historique.append({
                    "Date": date_du_jour,
                    "Exercice": ex_nom,
                    "Performance": details
                })
            st.success("Séance enregistrée dans l'historique !")

# --- 2. CRÉER UN EXERCICE ---
with tab2:
    st.header("Ajouter un nouvel exercice")
    
    nouveau_nom = st.text_input("Nom de l'exercice (ex: Squats, Fentes...)")
    type_ex = st.radio("Type de mesure :", ["Répétitions", "Chrono (sec)"])
    
    if st.button("Ajouter l'exercice"):
        if nouveau_nom.strip():
            st.session_state.exercices.append({"nom": nouveau_nom, "type": type_ex})
            st.success(f"Exercice '{nouveau_nom}' ajouté !")
            st.rerun()
        else:
            st.error("Renseigne un nom d'exercice.")

# --- 3. HISTORIQUE ---
with tab3:
    st.header("Historique de progression")
    
    if st.session_state.historique:
        df = pd.DataFrame(st.session_state.historique)
        st.dataframe(df, use_container_width=True)
        
        # Option pour vider l'historique
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.historique = []
            st.rerun()
    else:
        st.info("Aucune séance enregistrée pour le moment.")
