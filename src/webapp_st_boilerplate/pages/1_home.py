import streamlit as st

from webapp_st_boilerplate.auth.authorization import AuthManager
from webapp_st_boilerplate.front_end.cmd import FrontEnd


front_end_obj = FrontEnd(auth_manager=AuthManager())
front_end_obj.set_page_config(page_title="Streamlit Web App", page_icon="💻", layout="centered")
front_end_obj.set_sidebar()

st.title("Streamlit Web App")

st.markdown(
    """
    ## 👋 Benvenuto!

    [ADD DESCRIPTION WEBAPP]

    ---

    👉 Usa la barra laterale per navigare tra le principali funzionalità del sistema.
    """
)
