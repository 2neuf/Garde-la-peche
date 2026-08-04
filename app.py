import streamlit as st
import pandas as pd
from datetime import date
import time
import libsql_client

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sport", page_icon="🏋️")

# --- CONNEXION À TURSO VIA LIBSQL-CLIENT ---
@st.cache_resource
def get_client():
    url = st.secrets["TURSO_DATABASE_URL"]
    token = st.secrets["TURSO_AUTH_TOKEN"]
    # Conversion de l'URL 'libsql://' vers 'https://' pour l'API Https/Hrana
    if url.startswith("libsql://"):
        url = url.replace("libsql://", "https://")
    client = libsql_client.create_client_sync(url=url, auth_token=token)
    return client

client = get_client()

# Initialisation des tables SQLite dans Turso
def init_db():
    client.execute("""
        CREATE TABLE IF NOT EXISTS exercices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL
        )
    """)
    client.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercice TEXT NOT NULL,
            performance TEXT NOT NULL
        )
    """)

init_db()

# --- FONCTIONS DE GESTION DES DONNÉES ---
def get_exercices():
    rs = client.execute("SELECT nom, type FROM exercices")
    return [{"nom": row[0], "type": row[1]} for row in rs.rows]

def ajouter_exercice_db(nom, type_ex):
    client.execute("INSERT INTO exercices (nom, type) VALUES (?, ?)", (nom, type_ex))

def supprimer_exercice_db(nom):
    client.execute("DELETE FROM exercices WHERE nom = ?", (nom,))

def ajouter_historique_db(date_str, exercice, performance):
    client.execute("INSERT INTO historique (date, exercice, performance) VALUES (?, ?, ?)", (date_str, exercice, performance))

def get_historique_df():
    rs = client.execute("SELECT date as Date, exercice as Exercice, performance as Performance FROM historique ORDER BY id DESC")
    data = [dict(zip(["Date", "Exercice", "Performance"], row)) for row in rs.rows]
    return pd.DataFrame(data)

def supprimer_historique_db():
    client.execute("DELETE FROM historique")

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
            st.success(f"✅ Exercice '{nom_clean}' créé avec succès dans Turso !")
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
        
        form_data = {}
        
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
                ajouter_historique_db(date_du_jour, ex_nom, details)
                
            st.success("Séance enregistrée dans Turso !")
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
    
    df_hist = get_historique_df()
    if not df_hist.empty:
        st.dataframe(df_hist, use_container_width=True)
        
        if st.button("🗑️ Effacer tout l'historique"):
            supprimer_historique_db()
            st.toast("Historique réinitialisé.", icon="🧹")
            st.rerun()
    else:
        st.info("Aucune séance enregistrée pour le moment.")
