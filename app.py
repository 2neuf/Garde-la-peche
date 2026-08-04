import streamlit as st

st.set_page_config(
    page_title="Mes Séances",
    page_icon="💪",
    layout="centered"
)

# Style de la page d'accueil
st.markdown("""
<style>
.stApp {
    background-color: #000000;
}

.main-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 92vh;
}

.menu {
    width: 100%;
    max-width: 420px;
}

.stButton > button {
    width: 100%;
    height: 22vh;
    margin-bottom: 3vh;
    border-radius: 28px;
    border: none;
    background-color: #FFD400;
    color: #000000;
    font-size: 2rem;
    font-weight: 800;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #FFE04D;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container"><div class="menu">', unsafe_allow_html=True)

if st.button("EXERCICES"):
    st.switch_page("pages/1_Exercices.py")

if st.button("SÉANCES"):
    st.switch_page("pages/2_Seances.py")

if st.button("HISTORIQUE"):
    st.switch_page("pages/3_Historique.py")

st.markdown('</div></div>', unsafe_allow_html=True)