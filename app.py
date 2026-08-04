import streamlit as st

st.set_page_config(
    page_title="Mes Séances",
    page_icon="💪",
    layout="centered"
)

# Navigation interne
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Style global
st.markdown("""
<style>
.stApp {
    background-color: #000000;
}

.block-container {
    max-width: 500px;
    margin: auto;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label, span, div {
    color: white !important;
}

/* Gros boutons accueil */
.big-btn > button {
    width: 100% !important;
    height: 180px !important;
    margin-bottom: 24px !important;
    border-radius: 28px !important;
    border: none !important;
    background: #FFD400 !important;
    color: #000000 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

/* Boutons normaux */
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

    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    if st.button("EXERCICES"):
        st.session_state.page = "exercices"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    if st.button("SÉANCES"):
        st.session_state.page = "seances"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
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
        <div style="background:#111;padding:18px;border-radius:18px;border:1px solid #222;">
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