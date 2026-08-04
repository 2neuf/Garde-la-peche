import streamlit as st

st.set_page_config(
    page_title="Mes Séances",
    page_icon="💪",
    layout="centered"
)

st.markdown("""
<style>
/* Fond noir */
.stApp {
    background-color: #000000;
}

/* Zone centrale */
.block-container {
    max-width: 500px;
    margin: auto;
    padding-top: 5vh;
    padding-bottom: 5vh;
}

/* Boutons */
.stButton > button {
    display: block;
    width: 90vw;
    max-width: 420px;
    height: 24vh;
    margin: 0 auto 3vh auto;
    border-radius: 32px;
    border: none;
    background-color: #FFD400;
    color: #000000;
    font-size: 2rem;
    font-weight: 800;
    box-shadow: 0 0 20px rgba(255,212,0,0.15);
}

/* Hover */
.stButton > button:hover {
    background-color: #FFE04D;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

st.write("")

st.page_link("pages/1_Exercices.py", label="EXERCICES", icon="🏋️")
st.page_link("pages/2_Seances.py", label="SÉANCES", icon="🔥")
st.page_link("pages/3_Historique.py", label="HISTORIQUE", icon="📅")