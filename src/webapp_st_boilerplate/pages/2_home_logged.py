import streamlit as st

from webapp_st_boilerplate.auth.authorization import AuthManager
from webapp_st_boilerplate.front_end.cmd import FrontEnd


front_end_obj = FrontEnd(auth_manager=AuthManager())
front_end_obj.set_page_config(
    page_title="Home - Utente Loggato", page_icon="👤", layout="centered"
)
front_end_obj.set_sidebar()


st.title("👤 Benvenuto nella tua area personale!")

st.markdown(
    """
    Ciao! Sei autenticato e puoi ora usare le funzioni della webapp.

    ### 📚 Navigazione rapida
    Qui sotto trovi le pagine disponibili e le loro funzionalità:

    [ADD DESCRIPTION PAGES]

    ---

    Usa la barra laterale a sinistra per accedere rapidamente alle varie sezioni.

    > Nuove funzionalità saranno aggiunte prossimamente!
    """
)
