import streamlit as st
import pandas as pd
from datetime import date
import time

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sport", page_icon="🏋️")

st.title("🏋️ Mon Suivi de Sport")

# Initialisation des données locales
if "exercices" not in st.session_state:
    st.session_state.exercices = [
        {"nom": "Pompes", "type": "Répétitions"},
        {"nom": "Gainage", "type": "Chrono (sec)"}
    ]

if "historique" not in st.session_state:
    st.session_state.historique = []

if "tmp_nom_exercice" not in st.session_state:
    st.session_state.tmp_nom_exercice = ""

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🏋️ Entraînement", "⚙️ Gérer les Exercices", "📊 Historique"])

# --- 1. S'ENTRAÎNER ---
with tab1:
    st.header("Nouvelle séance")
    
    if not st.session_state.exercices:
        st.warning("Commence par créer un exercice dans l'onglet dédié !")
    else:
        noms_ex = [ex["nom"] for ex in st.session_state.exercices]
        ex_selectionnes = st.multiselect("Choisis les exercices de la séance :", noms_ex, default=noms_ex)
        
        form_data = {}
        
        for idx, nom in enumerate(ex_selectionnes, start=1):
            ex_obj = next(item for item in st.session_state.exercices if item["nom"] == nom)
            st.subheader(f"👉 {nom}")
            
            nb_series = st.number_input(
                f"Nombre de séries pour {nom}", 
                min_value=1, max_value=10, value=3, 
                key=f"series_{nom}_{idx}"
            )
            
            if "Chrono" in ex_obj["type"]:
                durée = st.number_input(
                    f"Objectif par série (secondes) :", 
                    min_value=5, value=30, step=5, 
                    key=f"target_{nom}_{idx}"
                )
                if st.button(f"⏱️ Lancer le chrono ({durée}s)", key=f"btn_{nom}_{idx}"):
                    progress_bar = st.progress(0)
                    for t in range(durée):
                        time.sleep(1)
                        progress_bar.progress((t + 1) / durée)
                    st.success("Terminé ! 🔥")
                
                form_data[nom] = f"{nb_series} séries de {durée}s"
            else:
                reps = st.number_input(
                    f"Répétitions par série :", 
                    min_value=1, value=10, 
                    key=f"reps_{nom}_{idx}"
                )
                form_data[nom] = f"{nb_series} séries de {reps} reps"

        if st.button("✅ Valider et enregistrer la séance", type="primary"):
            date_du_jour = date.today().strftime("%d/%m/%Y")
            for ex_nom, details in form_data.items():
                st.session_state.historique.append({
                    "Date": date_du_jour,
                    "Exercice": ex_nom,
                    "Performance": details
                })
            st.toast("Séance enregistrée avec succès !", icon="🎉")

# --- 2. CRÉER / SUPPRIMER UN EXERCICE ---
with tab2:
    st.header("Ajouter un nouvel exercice")
    
    nouveau_nom = st.text_input(
        "Nom de l'exercice (ex: Squats, Fentes...)", 
        value=st.session_state.tmp_nom_exercice
    )
    type_ex = st.radio("Type de mesure :", ["Répétitions", "Chrono (sec)"])
    
    if st.button("➕ Ajouter l'exercice"):
        nom_clean = nouveau_nom.strip()
        # Liste des noms existants en minuscules
        noms_existants = [ex["nom"].lower() for ex in st.session_state.exercices]
        
        if not nom_clean:
            st.error("Renseigne un nom d'exercice.")
        elif nom_clean.lower() in noms_existants:
            # Blocage des doublons ici
            st.warning(f"L'exercice '{nom_clean}' existe déjà !")
        else:
            st.session_state.exercices.append({"nom": nom_clean, "type": type_ex})
            st.toast(f"Exercice '{nom_clean}' créé avec succès !", icon="✅")
            st.session_state.tmp_nom_exercice = ""
            st.rerun()

    st.divider()

    st.header("Supprimer un exercice")
    if st.session_state.exercices:
        noms_existants_affichages = [ex["nom"] for ex in st.session_state.exercices]
        ex_a_supprimer = st.selectbox("Sélectionne l'exercice à retirer :", noms_existants_affichages, key="select_del")
        
        if st.button("🗑️ Supprimer cet exercice"):
            st.session_state.exercices = [ex for ex in st.session_state.exercices if ex["nom"] != ex_a_supprimer]
            st.toast(f"Exercice '{ex_a_supprimer}' supprimé.", icon="🗑️")
            st.rerun()

# --- 3. HISTORIQUE ---
with tab3:
    st.header("Historique de progression")
    
    if st.session_state.historique:
        df = pd.DataFrame(st.session_state.historique)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Effacer tout l'historique"):
            st.session_state.historique = []
            st.toast("Historique réinitialisé.", icon="🧹")
            st.rerun()
    else:
        st.info("Aucune séance enregistrée pour le moment.")
