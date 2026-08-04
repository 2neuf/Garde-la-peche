import streamlit as st

st.set_page_config(page_title="Mes Séances", page_icon="💪", layout="centered")

# État de navigation
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Style général
st.markdown("""
<style>
.stApp { background: #000000; }

.block-container {
    max-width: 500px;
    margin: auto;
    padding-top: 5vh;
    padding-bottom: 5vh;
}

/* Gros boutons accueil */
.big-button button {
    width: 100%;
    height: 22vh;
    margin-bottom: 3vh;
    border-radius: 32px;
    border: none;
    background: #FFD400;
    color: #000;
    font-size: 2rem;
    font-weight: 800;
}

/* Boutons classiques */
.stButton > button {
    width: 100%;
    border-radius: 16px;
    background: #FFD400;
    color: #000;
    font-weight: 700;
}

h1,h2,h3,p,label,span,div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ACCUEIL ----------------
if st.session_state.page == "accueil":

    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("EXERCICES"):
        st.session_state.page = "exercices"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("SÉANCES"):
        st.session_state.page = "seances"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("HISTORIQUE"):
        st.session_state.page = "historique"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- EXERCICES ----------------
elif st.session_state.page == "exercices":

    st.title("EXERCICES")

    nom = st.text_input("Nom de l'exercice", placeholder="Gainage")
    type_exo = st.selectbox("Type", ["Chrono", "Répétitions"])
    valeur = st.number_input("Valeur cible", min_value=1, value=30)

    if st.button("Ajouter l'exercice"):
        st.success(f"Exercice ajouté : {nom}")

    st.divider()

    st.markdown(
        '<div style="background:#111;padding:15px;border-radius:16px;margin-bottom:10px;border:1px solid #222;"><b>Gainage</b><br>30 s</div>',
        unsafe_allow_html=True,
    )

    if st.button("⬅ Retour à l'accueil"):
        st.session_state.page = "accueil"
        st.rerun()

# ---------------- SÉANCES ----------------
elif st.session_state.page == "seances":

    st.title("SÉANCES")

    st.text_input("Nom de la séance")
    st.selectbox("Exercice", ["Gainage"])
    st.number_input("Séries", min_value=1, value=3)

    if st.button("Ajouter à la séance"):
        st.success("Ajouté")

    st.divider()

    st.markdown(
        '<div style="background:#111;padding:15px;border-radius:16px;border:1px solid #222;"><b>Séance matin</b><br>Gainage 30 s × 3 séries</div>',
        unsafe_allow_html=True,
    )

    if st.button("Lancer la séance"):
        st.info("Le chrono sera ajouté ensuite")

    if st.button("⬅ Retour à l'accueil"):
        st.session_state.page = "accueil"
        st.rerun()

# ---------------- HISTORIQUE ----------------
elif st.session_state.page == "historique":

    st.title("HISTORIQUE")

    st.markdown(
        '<div style="background:#111;padding:15px;border-radius:16px;border:1px solid #222;">📅 04/08/2026 — Séance matin</div>',
        unsafe_allow_html=True,
    )

    if st.button("⬅ Retour à l'accueil"):
        st.session_state.page = "accueil"
        st.rerun()