from time import sleep

import streamlit as st

from webapp_st_boilerplate.auth.authorization import AuthManager
from webapp_st_boilerplate.auth.login import login
from webapp_st_boilerplate.db.gateway import DBGateway


class FrontEnd:
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.db_gateway = DBGateway()
        self._name: str | None = self._get_name()
        self._role_number: int | None = self._get_role_number()
        self._user_id: int | None = self._get_user_id()

    def _get_name(self) -> int | None:
        return st.session_state.get("user_name", None)

    def _get_role_number(self) -> int | None:
        return st.session_state.get("role_number", None)

    def _get_user_id(self) -> int | None:
        return st.session_state.get("user_id", None)

    def _can_show_page(self) -> bool:
        if self._user_id is None:
            st.warning("Non sei loggato, verrai reindirizzato alla pagina di login")
            with st.spinner():
                sleep(2)
            st.switch_page("pages/0_login.py")
        else:
            return True

    def _can_show_module(self, method_name: str) -> bool:
        self.auth_manager.can_access(user_current_level=self._role_number, method_name=method_name)

    def set_login_page(self):
        self.set_page_config(page_name="Login")
        self.set_sidebar()
        with st.container():
            _, middle_col, _ = st.columns(3)
        with middle_col:
            st.subheader("Login")
            with st.form("login_form", clear_on_submit=True):
                user_email = st.text_input("Email")
                user_psw = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Entra")
            if login_button:
                (user_exist, wrong_password, role_number, name, user_id) = login(
                    email=user_email, password=user_psw
                )
                if not user_exist:
                    st.warning("L'email inserita non è registrata")
                if wrong_password:
                    st.warning("Password errata")
                if (user_exist) and (not wrong_password):
                    st.success(
                        "Credenziali corrette, a breve verrai reindirizzato nell'applicazione"
                    )
                    st.session_state["user_name"] = name
                    st.session_state["role_number"] = role_number
                    st.session_state["user_id"] = user_id
                    with st.spinner():
                        sleep(2)

    def set_page_config(self, page_name: str):
        st.set_page_config(page_title=page_name)

    def set_sidebar(self):
        pass
