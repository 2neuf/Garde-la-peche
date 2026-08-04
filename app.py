import streamlit as st
import pandas as pd
from datetime import date
import time
import requests

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sport", page_icon="🏋️")

# --- FONCTION REQUÊTE TURSO API HTTP ---
def turso_query(statements):
    """Exécute des requêtes SQL sur la base Turso via l'API HTTP Pipeline."""
    url = st.secrets["TURSO_DATABASE_URL"]
    token = st.secrets["TURSO_AUTH_TOKEN"]
    
    # Nettoyage de l'URL pour l'API HTTP
    url = url.replace("libsql://", "https://").replace("https://https://", "https://")
    api_url = f"{url}/v2/pipeline"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    requests_payload = []
    for stmt in statements:
        if isinstance(stmt, str):
            requests_payload.append({"type": "execute", "stmt": {"sql": stmt}})
        elif isinstance(stmt, tuple):
            sql, args = stmt
            formatted_args = []
            for arg in args:
                formatted_args.append({"type": "text", "value": str(arg)})
            requests_payload.append({"type": "execute", "stmt": {"sql": sql, "args": formatted_args}})

    payload = {"requests": requests_payload}
    
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Initialisation des tables SQLite dans Turso
def init_db():
    queries = [
        "CREATE TABLE IF NOT EXISTS exercices (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT UNIQUE NOT NULL, type TEXT NOT NULL);",
        "CREATE TABLE IF NOT EXISTS historique (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, detail TEXT NOT NULL);"
    ]
    turso_query(queries)


init_db()

# --- FONCTIONS DE GESTION DES DONNÉES ---
def get_exercices():
    res = turso_query(["SELECT nom, type FROM exercices"])
    results = res["results"][0]["response"]["result"]
    rows = results.get("rows", [])
    exercices = []
    for row in rows:
        exercices.append({"nom": row[0]["value"], "type": row[1]["value"]})
    return exercices

def ajouter_exercice_db(nom, type_ex):
    turso_query([("INSERT INTO exercices (nom, type) VALUES (?, ?)", (nom, type_ex))])

def supprimer_exercice_db(nom):
    turso_query([("DELETE FROM exercices WHERE nom = ?", (nom,))])

def ajouter_historique_db(date_str, detail_seance):
    turso_query([("INSERT INTO historique (date, detail) VALUES (?, ?)", (date_str, detail_seance))])

def get_historique_df():
    res = turso_query(["SELECT date, detail FROM historique ORDER BY id DESC"])
    results = res["results"][0]["response"]["result"]
    rows = results.get("rows", [])
    data = []
    for row in rows:
        data.append({
            "Date": row[0]["value"],
            "Séance détaillée": row[1]["value"]
        })
    return pd.DataFrame(data)

def supprimer_historique_db():
    turso_query(["DELETE FROM historique"])

# --- INITIALISATION SESSION STATE ---
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if "page" not in st.session_state:
    st.session_state.page = "accueil"

# --- PAGE D'ACCUEIL ---
if st.session_state.page == "accueil":
    st.title("🏋️ Mon Suivi de Sport")
    st.write("Que veux-tu faire aujourd'hui ?")
    
    st.divider()
    
    if st.button("➕ Créer exercice", use_container_width=True):
        st.session_state.page = "creer_exercice"
        st.rerun()
        
    if st.button("🏋️ Créer séance", type="primary", use_container_width=True):
        st.session_state.page = "creer_seance"
        st.rerun()
        
    if st.button("📊 Voir historique", use_container_width=True):
        st.session_state.page = "historique"
        st.rerun()

# --- PAGE 1 : CRÉER / GÉRER EXERCICE ---
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
        exercices_existants = get_exercices()
        noms_existants = [ex["nom"].lower() for ex in exercices_existants]
        
        if not nom_clean:
            st.error("Renseigne un nom d'exercice.")
        elif nom_clean.lower() in noms_existants:
            st.warning(f"L'exercice '{nom_clean}' existe déjà !")
        else:
            ajouter_exercice_db(nom_clean, type_ex)
            st.success(f"✅ Exercice '{nom_clean}' créé avec succès !")
            st.toast(f"Exercice '{nom_clean}' créé !", icon="✅")
            st.session_state.reset_counter += 1
            time.sleep(1)
            st.rerun()

    st.divider()

    st.subheader("Supprimer un exercice")
    exercices = get_exercices()
    if exercices:
        noms_existants_affichages = [ex["nom"] for ex in exercices]
        ex_a_supprimer = st.selectbox("Sélectionne l'exercice à retirer :", noms_existants_affichages, key="select_del")
        
        if st.button("🗑️ Supprimer cet exercice"):
            supprimer_exercice_db(ex_a_supprimer)
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
    
    exercices = get_exercices()
    if not exercices:
        st.warning("Commence par créer un exercice !")
    else:
        noms_ex = [ex["nom"] for ex in exercices]
        ex_selectionnes = st.multiselect("Choisis les exercices de la séance :", noms_ex, default=noms_ex)
        
        details_exercices = []
        
        for idx, nom in enumerate(ex_selectionnes, start=1):
            ex_obj = next(item for item in exercices if item["nom"] == nom)
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
                
                details_exercices.append(f"{nom}: {nb_series}x{durée}s")
            else:
                reps = st.number_input(
                    f"Répétitions par série :", 
                    min_value=1, value=10, 
                    key=f"reps_{nom}_{idx}"
                )
                details_exercices.append(f"{nom}: {nb_series}x{reps} reps")

        if st.button("✅ Enregistrer la séance", type="primary", use_container_width=True):
            if details_exercices:
                date_du_jour = date.today().strftime("%d/%m/%Y")
                # Regroupement de tous les exercices sur une seule ligne (ex: "Pompes: 3x10 reps | Gainage: 3x30s")
                resume_seance = " | ".join(details_exercices)
                
                ajouter_historique_db(date_du_jour, resume_seance)
                
                st.success("Séance enregistrée !")
                st.toast("Séance enregistrée !", icon="🎉")
                time.sleep(1)
                st.session_state.page = "historique"
                st.rerun()
            else:
                st.error("Sélectionne au moins un exercice.")

# --- PAGE 3 : HISTORIQUE ---
elif st.session_state.page == "historique":
    if st.button("⬅️ Retour au menu"):
        st.session_state.page = "accueil"
        st.rerun()
        
    st.title("📊 Historique de Progression")
    
    df_hist = get_historique_df()
    if not df_hist.empty:
        st.dataframe(df_hist, use_container_width=True)
        
        if st.button("🗑️ Effacer tout l'historique"):
            supprimer_historique_db()
            st.toast("Historique réinitialisé.", icon="🧹")
            st.rerun()
    else:
        st.info("Aucune séance enregistrée pour le moment.")
