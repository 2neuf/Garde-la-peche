import streamlit as st

st.set_page_config(page_title="Historique", page_icon="📅")

st.markdown("""
<style>
.stApp {background:#000;}
h1,h2,h3,p,label,span,div {color:white !important;}
</style>
""", unsafe_allow_html=True)

st.title("HISTORIQUE")

st.info("Cette page affichera l'historique de tes séances.")