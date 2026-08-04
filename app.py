
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(page_title="Mes Séances", page_icon="💪", layout="centered")

DATA = Path("data.json")

def load_data():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return {"exercices": [], "seances": [], "historique": []}

def save_data(data):
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

data = load_data()

st.markdown("""
<style>
.stApp {background:#000;color:#fff;}
h1,h2,h3,p,label,span,div {color:#fff!important;}
.stButton>button {
    width:100%;
    background:#FFD400;
    color:#000;
    border:none;
    border-radius:16px;
    padding:0.8rem;
    font-weight:700;
}
.block-container {padding-top:1rem;}
.card {
    background:#111;
    padding:1rem;
    border-radius:18px;
    border:1px solid #222;
    margin-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("MES SÉANCES")

page = st.radio(
    "",
    ["Exercices", "Séances", "Historique"],
    horizontal=True,
)

if page == "Exercices":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Créer un exercice")
    nom = st.text_input("Nom", placeholder="Gainage")
    typ = st.selectbox("Type", ["chrono", "repetitions"])
    valeur = st.number_input("Valeur cible", min_value=1, value=30)
    if st.button("Ajouter l'exercice"):
        data["exercices"].append({"nom": nom, "type": typ, "valeur": int(valeur)})
        save_data(data)
        st.success("Exercice ajouté")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Mes exercices")
    if not data["exercices"]:
        st.info("Aucun exercice")
    for exo in data["exercices"]:
        unite = "s" if exo["type"] == "chrono" else "reps"
        st.markdown(f'<div class="card">**{exo["nom"]}** — {exo["valeur"]} {unite}</div>', unsafe_allow_html=True)

elif page == "Séances":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Créer une séance")
    nom_seance = st.text_input("Nom de la séance")

    if "temp" not in st.session_state:
        st.session_state.temp = []

    if data["exercices"]:
        options = [e["nom"] for e in data["exercices"]]
        choix = st.selectbox("Exercice", options)
        series = st.number_input("Nombre de séries", min_value=1, value=3)

        if st.button("Ajouter à la séance"):
            exo = next(e for e in data["exercices"] if e["nom"] == choix)
            st.session_state.temp.append({**exo, "series": int(series)})
            st.rerun()

    if st.session_state.temp:
        st.write("Exercices de la séance")
        for e in st.session_state.temp:
            unite = "s" if e["type"] == "chrono" else "reps"
            st.write(f"- {e['nom']} : {e['valeur']} {unite} × {e['series']}")

        if st.button("Enregistrer la séance"):
            data["seances"].append({
                "nom": nom_seance,
                "exercices": st.session_state.temp
            })
            st.session_state.temp = []
            save_data(data)
            st.success("Séance enregistrée")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Séances enregistrées")
    if not data["seances"]:
        st.info("Aucune séance")
    else:
        for i, s in enumerate(data["seances"]):
            st.markdown(f'<div class="card"><h3>{s["nom"]}</h3></div>', unsafe_allow_html=True)
            if st.button(f"Lancer {s['nom']}", key=f"run_{i}"):
                st.session_state.run = i

    if "run" in st.session_state:
        s = data["seances"][st.session_state.run]
        st.divider()
        st.header(f"Séance : {s['nom']}")

        for exo in s["exercices"]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(exo["nom"])
            for serie in range(exo["series"]):
                st.write(f"Série {serie+1}/{exo['series']}")

                if exo["type"] == "chrono":
                    timer_placeholder = st.empty()
                    for sec in range(exo["valeur"], -1, -1):
                        timer_placeholder.markdown(
                            f"<h1 style='text-align:center;color:#FFD400'>{sec}</h1>",
                            unsafe_allow_html=True
                        )
                        time.sleep(1)
                    st.success("Temps terminé")
                else:
                    st.markdown(
                        f"<h1 style='text-align:center;color:#FFD400'>{exo['valeur']} répétitions</h1>",
                        unsafe_allow_html=True
                    )
                    st.button("Série terminée", key=f"{exo['nom']}_{serie}")

            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Terminer la séance"):
            data["historique"].insert(0, {
                "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "seance": s["nom"]
            })
            save_data(data)
            del st.session_state.run
            st.success("Séance enregistrée dans l'historique")
            st.rerun()

elif page == "Historique":
    st.subheader("Historique")
    if not data["historique"]:
        st.info("Aucune séance réalisée")
    else:
        for h in data["historique"]:
            st.markdown(
                f'<div class="card">📅 **{h["date"]}** — {h["seance"]}</div>',
                unsafe_allow_html=True
            )
