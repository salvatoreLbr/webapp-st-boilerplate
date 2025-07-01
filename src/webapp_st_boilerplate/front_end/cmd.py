from time import sleep

import streamlit as st

from webapp_st_boilerplate.auth.authorization import AuthManager
from webapp_st_boilerplate.auth.login import change_password, login
from webapp_st_boilerplate.cmd_handler import Cmd
from webapp_st_boilerplate.db.gateway import DBGateway


class FrontEnd:
    def __init__(self, auth_manager: AuthManager):
        self._auth_manager = auth_manager
        self._db_gateway = DBGateway()
        self._name: str | None = self._get_name()
        self._role_number: int | None = self._get_role_number()
        self._user_id: int | None = self._get_user_id()
        self._entity_id: int | None = self._get_entity_id()
        self._cmd = Cmd(user_id=self._user_id, entity_id=self._entity_id)

    def _get_entity_id(self) -> int | None:
        return st.session_state.get("entity_id", None)

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
        return self._auth_manager.can_access(
            user_current_level=self._role_number, method_name=method_name
        )

    def _set_credential(self, name: str, role_number: int, user_id: int, entity_id: int):
        st.session_state["user_name"] = name
        st.session_state["role_number"] = role_number
        st.session_state["user_id"] = user_id
        st.session_state["entity_id"] = entity_id
        self._cmd = Cmd(user_id=user_id, entity_id=entity_id)

    def set_admin_page(self):  # noqa: PLR0912, PLR0915
        self.set_page_config(page_title="Pannello Admin", page_icon="👮‍♂️", layout="centered")
        self.set_sidebar()

        st.title("👮‍♂️ Pannello di Amministrazione")
        st.markdown(
            """
            In questa pagina puoi: \n
            - visualizzare le entità e gli utenti presenti nel database
            - creare una nuova entità aziendale
            - aggiungere nuovi utenti al sistema
            - disabilitare un utente
            """
        )

        #: Get entity_df and user_df
        entities_df = self._cmd.get_entity()
        if not entities_df.empty:
            st.subheader("Entità presenti nel DB")
            st.dataframe(entities_df, hide_index=True)
        else:
            st.warning("Non ci sono entità presenti nel DB")
        users_df = self._cmd.get_users()
        if not users_df.empty:
            st.subheader("Utenti registrati nel DB")
            st.dataframe(
                users_df[
                    [
                        "entityId",
                        "name",
                        "role",
                        "disabled",
                        "lastLogin",
                        "createdDate",
                        "updatedDate",
                    ]
                ],
                hide_index=True,
            )
        else:
            st.warning("Non ci sono utenti registrati nel DB")

        #: Show form to create a new entity
        if self._can_show_module(method_name="create_entity"):
            st.subheader("🏢 Crea una nuova Entity")
            with st.form("create_entity_form"):
                entity_name = st.text_input("Nome entità aziendale")
                submit_entity = st.form_submit_button("Crea Entity")
                if submit_entity:
                    entity_dict = {
                        "entityName": entity_name,
                    }
                    created, msg = self._cmd.create_entity(entity_dict=entity_dict)
                    if created:
                        st.success(f"Entità '{entity_name}' creata con successo!")
                        sleep(2)
                        st.switch_page("pages/3_admin.py")
                    else:
                        st.error(f"Errore nella creazione dell'entità: {msg}")

        #: Show form to create a new user
        if self._can_show_module("create_user"):
            st.subheader("👤 Crea un nuovo Utente")
            if entities_df.empty:
                st.warning("""
                    Nessuna entity registrata nel database.
                    Crea prima un'entity per poter creare un nuovo utente
                """)
            else:
                with st.form("create_user_form"):
                    user_name = st.text_input("Nome utente")
                    user_email = st.text_input("Email")
                    user_password = st.text_input("Password", type="password")
                    user_role = st.selectbox(
                        label="Ruolo", options=["USER", "USER_ADMIN", "ADMIN"]
                    )
                    user_entity = st.selectbox(
                        label="Entity", options=list(entities_df["entityName"].unique())
                    )
                    submit_user = st.form_submit_button("Crea Utente")
                    if submit_user:
                        user_dict = {
                            "name": user_name,
                            "email": user_email,
                            "password": user_password,
                            "role": user_role,
                            "disabled": False,
                        }
                        entity_id = int(
                            entities_df.loc[entities_df["entityName"] == user_entity, "id"].values[
                                0
                            ]
                        )
                        created, msg = self._cmd.create_user(
                            user_dict=user_dict, entity_id=entity_id
                        )
                        if created:
                            st.success(f"Utente '{user_name}' creato con successo!")
                            sleep(2)
                            st.switch_page("pages/3_admin.py")
                        else:
                            st.error(f"Errore nella creazione dell'utente: {msg}")

        #: Show form to disable an user
        if self._can_show_module("disable_user"):
            st.subheader("🚷 Disabilita un Utente")
            if users_df.empty:
                st.warning("""
                    Nessun utente registrato nel database.
                """)
            else:
                with st.form("disable_user"):
                    user_name = st.selectbox(
                        label="Utente da disabilitare", options=list(users_df["name"].unique())
                    )
                    submit_disable = st.form_submit_button("Disabilita")
                    if submit_disable:
                        user_id_to_disable = int(users_df.loc[users_df["name"] == user_name, "id"])
                        disabled, msg = self._cmd.disable_user(user_id=user_id_to_disable)
                        if disabled:
                            st.success(f"Utente '{user_name}' disabilitato con successo!")
                            sleep(2)
                            st.switch_page("pages/3_admin.py")
                        else:
                            st.error(f"Errore nel disabilitare l'utente: {msg}")

    def set_login_page(self):
        self.set_page_config(page_title="Login", page_icon="🔓", layout="centered")
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
                (user_exist, wrong_password, disabled, role_number, name, user_id, entity_id) = (
                    login(email=user_email, password=user_psw)
                )
                if not user_exist:
                    st.warning("L'email inserita non è registrata")
                if wrong_password:
                    st.warning("Password errata")
                if disabled:
                    st.warning("Utente disabilitato, non puoi accedere")
                if (user_exist) and (not wrong_password) and (not disabled):
                    st.success(
                        "Credenziali corrette, a breve verrai reindirizzato nell'applicazione"
                    )
                    self._set_credential(
                        name=name,
                        role_number=role_number,
                        user_id=user_id,
                        entity_id=entity_id,
                    )
                    with st.spinner():
                        sleep(2)
                        st.switch_page("pages/2_home_logged.py")

    def set_page_config(self, page_title: str, page_icon: str, layout: str):
        st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

    def set_sidebar(self):
        with st.sidebar:
            if self._user_id is None:
                if st.button("🏠 Home"):
                    st.switch_page("pages/1_home.py")
                if st.button("🔓 Login"):
                    st.switch_page("pages/0_login.py")
            if self._user_id is not None:
                if st.button("🏠 Home"):
                    st.switch_page("pages/2_home_logged.py")
                if self._role_number >= 3:
                    admin_page_button = st.button("👮‍♂️Admin")
                    if admin_page_button:
                        st.switch_page("pages/3_admin.py")
                user_panel_button = st.button("⚙️Impostazioni")
                if user_panel_button:
                    st.switch_page("pages/4_user_panel.py")
                if st.button("🔐 Logout"):
                    st.session_state["user_name"] = None
                    st.session_state["role_number"] = None
                    st.session_state["user_id"] = None
                    self._user_name = None
                    self._role_number = None
                    self._user_id = None
                    st.switch_page("pages/1_home.py")

    def set_user_panel(self):
        self.set_page_config(page_title="Impostazioni", page_icon="👮‍♂️", layout="centered")
        self.set_sidebar()

        st.title("👮‍♂️ Impostazioni")
        st.markdown(
            """
            In questa pagina puoi cambiare la tua password
            """
        )

        #: Get users_df and filter by actual user
        users_df = self._cmd.get_users()
        users_df = users_df.loc[users_df["id"] == self._user_id]

        with st.form("change_password"):
            email = st.text_input(label="Inserisci l'email dell'account")
            old_password = st.text_input(label="Attuale password", type="password")
            new_password = st.text_input(label="Nuova password", type="password")
            repeat_new_password = st.text_input(label="Ripeti la nuova password", type="password")
            submit_change_password = st.form_submit_button("Aggiorna password")
            if submit_change_password:
                if repeat_new_password != new_password:
                    st.warning("Le password nuove non coincidono")
                else:
                    updated, msg = change_password(
                        email=email, old_password=old_password, new_password=new_password
                    )
                    if updated:
                        st.success("Password aggiornata con successo")
                        sleep(2)
                        st.switch_page("pages/2_home_logged.py")
                    else:
                        st.error(f"Password non aggiornata per il seguente motivo: {msg}")
