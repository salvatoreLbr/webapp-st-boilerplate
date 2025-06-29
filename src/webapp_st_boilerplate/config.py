import streamlit as st

from pydantic import BaseModel
from pydantic_settings import BaseSettings


db_secrets = st.secrets.get("db", {})
login_secrets = st.secrets.get("login", {})


class DBSecrets(BaseModel):
    db_encryption_key: str = db_secrets.get("db_encryption_key", "")
    db_name: str = db_secrets.get("db_name", "")
    db_password: str = db_secrets.get("db_password", "")
    db_url: str = db_secrets.get("db_url", "sqlite:///./webapp_st_boilerplate.db")
    db_user: str = db_secrets.get("db_user", "")


class LoginSecrets(BaseModel):
    algorithm: str = login_secrets.get("algorithm", "algorithm")
    login_secret_key: str = login_secrets.get("login_secret_key", "login_secret_key")
    rounds: int = login_secrets.get("rounds", 0)


class Settings(BaseSettings):
    db_secrets: DBSecrets = DBSecrets()
    login_secrets: LoginSecrets = LoginSecrets()


settings = Settings()
