import re

import pandas as pd

from passlib.hash import bcrypt

from webapp_st_boilerplate.auth.authorization import Role
from webapp_st_boilerplate.config import settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.login_secrets.login_secret_key
ALGORITHM = settings.login_secrets.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 10 * 365 * 24 * 60

# Initialize CryptContext/bcrypt
pwd_context = bcrypt.using(rounds=settings.login_secrets.rounds)


def verify_hash(plain_phrase, hashed_phrase):
    return pwd_context.verify(plain_phrase, hashed_phrase)


def get_hash(phrase):
    return pwd_context.hash(phrase)


def authenticate(
    users_df: pd.DataFrame, email: str, password: str
) -> tuple[bool, bool, int, str, int]:
    """Given users dataframe, email and password authenticate user.
    Function return the following info:
    - user exist
    - wrong password
    - role (as number)
    - username
    - user_id

    Args:
        users_df (pd.DataFrame): _description_
        email (str): _description_
        password (str): _description_
    """
    #: Check if there is almost an user
    if users_df.shape[0] == 0:
        #: There aren't any user in table User
        return False, False, "", "", -9
    #: Get email if exists
    idx_email = users_df.email.apply(lambda x: verify_hash(email, x))
    if idx_email.sum() == 1:
        user_exist = True
    else:
        return False, False, "", "", -9
    #: Check password
    user_password = users_df.loc[idx_email, "password"].values[0]
    if verify_hash(password, user_password):
        wrong_password = False
    else:
        return user_exist, True, "", "", -9
    #: Get username and retrieve page
    name = users_df.loc[idx_email, "name"].values[0]
    role = users_df.loc[idx_email, "role"].values[0]
    role_number = Role._member_map_.get(role).value
    user_id = int(users_df.loc[idx_email, "id"].values[0])
    return user_exist, wrong_password, role_number, name, user_id


def check_rules_password(psw: str) -> tuple[bool, str]:
    error_in_psw = False
    type_response = "passwordchanged"
    if len(psw) < 8:
        # "La password deve essere lunga almeno 8 caratteri"
        type_response = "La password deve essere lunga almeno 8 caratteri"
        error_in_psw = True
    elif re.search("[0-9]", psw) is None:
        # "La password deve contenere almeno un numero"
        type_response = "La password deve contenere almeno un numero"
        error_in_psw = True
    elif re.search("[A-Z]", psw) is None:
        # "La password deve contenere almeno una lettera maiuscola"
        type_response = "La password deve contenere almeno una lettera maiuscola"
        error_in_psw = True

    return error_in_psw, type_response
