import streamlit as st
import pandas as pd
from datetime import date
import time

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sport", page_icon="🏋️")

# Initialisation des données locales
if "exercices" not in st.session_state:
    st.session_state.exercices = [
        {"nom": "Pompes", "type": "Répétitions"},
        {"nom": "Gainage", "type": "Chrono (sec)"}
    ]

if "historique" not in st.session_state:
    st.session_state.historique = []

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# Navigation principale via session_state
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# --- PAGE D'ACCUEIL ---
if st.session_state.page == "accueil":
    st.title("🏋️ Mon Suivi de Sport")
    st.write("Que veux-tu faire aujourd'hui ?")
    
    st.divider()
    
    # Les 3 boutons principaux
    if st.button("➕ Créer exercice", use_container_width=True):
        st.session_state.page = "creer_exercice"
        st.rerun()
        
    if st.button("🏋️ Créer séance", type="primary", use_container_width=True):
        st.session_state.page = "creer_seance"
        st.rerun()
        
    if st.button("📊 Voir historique", use_container_width=True):
        st.session_state.page = "historique"
        st.rerun()

# --- PAGE 1 : CRÉER EXERCICE ---
elif st.session_state.page == "creer_exercice":
    if st.button("⬅️ Retour au menu"):
        st.session_state.page = "accueil"
        st.rerun()
        
    st.title("➕ Gérer les Exercices")
    
    st.subheader("Ajouter un exercice")
    nouveau_nom = st.text_input(
        "Nom de l'exercice (ex: Squats, Fentes...)", 
        key=f"input_nom_{st.session_state.reset_counter}"
    )
    type_ex = st.radio("Type de mesure :", ["Répétitions", "Chrono (sec)"])
    
    if st.button("Valider l'ajout", type="primary"):
        nom_clean = nouveau_nom.strip()
        noms_existants = [ex["nom"].lower() for ex in st.session_state.exercices]
        
        if not nom_clean:
            st.error("Renseigne un nom d'exercice.")
        elif nom_clean.lower() in noms_existants:
            st.warning(f"L'exercice '{nom_clean}' existe déjà !")
        else:
            st.session_state.exercices.append({"nom": nom_clean, "type": type_ex})
            st.success(f"✅ Exercice '{nom_clean}' créé avec succès !")
            st.toast(f"Exercice '{nom_clean}' créé !", icon="✅")
            st.session_state.reset_counter += 1
            time.sleep(1)
            st.rerun()

    st.divider()

    st.subheader("Supprimer un exercice")
    if st.session_state.exercices:
        noms_existants_affichages = [ex["nom"] for ex in st.session_state.exercices]
        ex_a_supprimer = st.selectbox("Sélectionne l'exercice à retirer :", noms_existants_affichages, key="select_del")
        
        if st.button("🗑️ Supprimer cet exercice"):
            st.session_state.exercices = [ex for ex in st.session_state.exercices if ex["nom"] != ex_a_supprimer]
            st.toast(f"Exercice '{ex_a_supprimer}' supprimé.", icon="🗑️")
            st.rerun()
    else:
        st.info("Aucun exercice disponible.")

# --- PAGE 2 : CRÉER SÉANCE ---
elif st.session_state.page == "creer_seance":
    if st.button("⬅️ Retour au menu"):
        st.session_state.page = "accueil"
        st.rerun()
        
    st.title("🏋️ Nouvelle Séance")
    
    if not st.session_state.exercices:
        st.warning("Commence par créer un exercice !")
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

        if st.button("✅ Enregistrer la séance", type="primary", use_container_width=True):
            date_du_jour = date.today().strftime("%d/%m/%Y")
            for ex_nom, details in form_data.items():
                st.session_state.historique.append({
                    "Date": date_du_jour,
                    "Exercice": ex_nom,
                    "Performance": details
                })
            st.success("Séance enregistrée dans l'historique !")
            st.toast("Séance enregistrée !", icon="🎉")
            time.sleep(1)
            st.session_state.page = "historique"
            st.rerun()

# --- PAGE 3 : HISTORIQUE ---
elif st.session_state.page == "historique":
    if st.button("⬅️ Retour au menu"):
        st.session_state.page = "accueil"
        st.rerun()
        
    st.title("📊 Historique de Progression")
    
    if st.session_state.historique:
        df = pd.DataFrame(st.session_state.historique)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Effacer tout l'historique"):
            st.session_state.historique = []
            st.toast("Historique réinitialisé.", icon="🧹")
            st.rerun()
    else:
        st.info("Aucune séance enregistrée pour le moment.")
