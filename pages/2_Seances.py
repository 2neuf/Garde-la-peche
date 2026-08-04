import streamlit as st

st.set_page_config(page_title="Séances", page_icon="🔥")

st.markdown("""
<style>
.stApp {background:#000;}
h1,h2,h3,p,label,span,div {color:white !important;}
</style>
""", unsafe_allow_html=True)

st.title("SÉANCES")

st.info("Cette page servira à créer et lancer tes séances.")