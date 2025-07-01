import pandas as pd

from tests.test_webapp_st_boilerplate.test_db import (
    delete_database_tables,
    init_test_database,
)
from webapp_st_boilerplate.auth.authentication import authenticate
from webapp_st_boilerplate.db.gateway import DBGateway


def test_authenticate():
    init_test_database()
    #: Init test database
    db_gateway = DBGateway()
    users_df = db_gateway.get_user()
    #: Test authenticate
    (user_exist, wrong_password, _, role, name, _, _) = authenticate(
        users_df=users_df,
        email="test.user@example.com",
        password="Password123!",  # noqa: S106
    )
    assert user_exist, "Error in authenticate"
    assert not wrong_password, "Error in authenticate"
    assert role == 3, "Error in authenticate"
    assert name == "Test User", "Error in authenticate"

    (user_exist, _, _, _, _, _, _) = authenticate(
        users_df=users_df,
        email="prova@example.com",
        password="Password123!",  # noqa: S106
    )
    assert not user_exist, "Error in authenticate"

    (user_exist, wrong_password, _, _, _, _, _) = authenticate(
        users_df=users_df,
        email="test.user@example.com",
        password="Prova12!",  # noqa: S106
    )
    assert user_exist, "Error in authenticate"
    assert wrong_password, "Error in authenticate"

    delete_database_tables()

    (user_exist, wrong_password, _, _, _, _, _) = authenticate(
        users_df=pd.DataFrame(),
        email="test.user@example.com",
        password="Prova12!",  # noqa: S106
    )
    assert not user_exist, "Error in authenticate"
    assert not wrong_password, "Error in authenticate"
