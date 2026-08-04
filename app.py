import streamlit as st

st.set_page_config(
    page_title="Mes Séances",
    page_icon="💪",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #000000;
}

.block-container {
    padding-top: 8vh;
    padding-bottom: 8vh;
    max-width: 450px;
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
}

.stButton > button:hover {
    background-color: #FFE04D;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

st.write("")  # espace en haut

if st.button("EXERCICES"):
    st.switch_page("pages/1_Exercices.py")

if st.button("SÉANCES"):
    st.switch_page("pages/2_Seances.py")

if st.button("HISTORIQUE"):
    st.switch_page("pages/3_Historique.py")