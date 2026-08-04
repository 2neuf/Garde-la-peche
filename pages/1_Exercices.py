import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Exercices", page_icon="🏋️")

DATA = Path("data.json")

def load_data():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return {"exercices": []}

def save_data(data):
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

data = load_data()

st.markdown("""
<style>
.stApp {background:#000;}
h1,h2,h3,p,label,span,div {color:white !important;}
.stButton > button {
    width:100%;
    background:#FFD400;
    color:black;
    border:none;
    border-radius:16px;
    padding:0.8rem;
    font-weight:700;
}
.stTextInput input, .stNumberInput input {
    background:#111;
    color:white;
}
</style>
""", unsafe_allow_html=True)

st.title("EXERCICES")

nom = st.text_input("Nom de l'exercice", placeholder="Gainage")
type_exo = st.selectbox("Type", ["chrono", "repetitions"])
valeur = st.number_input("Valeur cible", min_value=1, value=30)

if st.button("Ajouter l'exercice"):
    data["exercices"].append({
        "nom": nom,
        "type": type_exo,
        "valeur": int(valeur)
    })
    save_data(data)
    st.success("Exercice ajouté")
    st.rerun()

st.divider()

st.subheader("Mes exercices")

if not data["exercices"]:
    st.info("Aucun exercice enregistré")
else:
    for exo in data["exercices"]:
        unite = "s" if exo["type"] == "chrono" else "reps"
        st.markdown(
            f"""
            <div style="background:#111;padding:15px;border-radius:16px;margin-bottom:10px;border:1px solid #222;">
                <b>{exo['nom']}</b><br>
                {exo['valeur']} {unite}
            </div>
            """,
            unsafe_allow_html=True
        )