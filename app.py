import streamlit as st

st.set_page_config(
    page_title="Mes Séances",
    page_icon="💪",
    layout="centered"
)

# Navigation interne
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# ---------------- STYLE GLOBAL ----------------
st.markdown("""
<style>

/* Fond noir */
.stApp {
    background-color: #000000;
}

/* Supprime les marges Streamlit */
.block-container {
    max-width: 100% !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Conteneur de la page d'accueil */
.main-menu {
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2vh;
}

/* Gros boutons jaunes */
.main-menu .stButton > button {
    width: 92vw !important;
    max-width: 480px !important;
    height: 26vh !important;
    border-radius: 32px !important;
    border: none !important;
    background: #FFD400 !important;
    color: #000000 !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    box-shadow: 0 0 25px rgba(255,212,0,0.18) !important;
}

/* Hover */
.main-menu .stButton > button:hover {
    background: #FFE04D !important;
    color: #000000 !important;
}

/* Texte blanc partout */
h1,h2,h3,p,label,span,div {
    color: white !important;
}

/* Boutons des pages internes */
.stButton > button {
    border-radius: 16px;
    background: #FFD400;
    color: #000000;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ---------------- ACCUEIL ----------------
if st.session_state.page == "accueil":

    st.markdown('<div class="main-menu">', unsafe_allow_html=True)

    if st.button("EXERCICES"):
        st.session_state.page = "exercices"
        st.rerun()

    if st.button("SÉANCES"):
        st.session_state.page = "seances"
        st.rerun()

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
        """
        <div style="background:#111;padding:18px;border-radius:18px;margin-bottom:12px;border:1px solid #222;">
            <b>Gainage</b><br>
            30 s
        </div>
        """,
        unsafe_allow_html=True
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
        st.success("Exercice ajouté à la séance")

    st.divider()

    st.markdown(
        """
        <div style="background:#111;padding:18px;border-radius:18px;border:1px solid #222;">
            <b>Séance matin</b><br>
            Gainage 30 s × 3 séries
        </div>
        """,
        unsafe_allow_html=True
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
        """
        <div style="background:#111;padding:18px;border-radius:18px;border:1px solid #222;">
            📅 04/08/2026 — Séance matin
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅ Retour à l'accueil"):
        st.session_state.page = "accueil"
        st.rerun()