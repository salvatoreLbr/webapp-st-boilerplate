from tests.test_webapp_st_boilerplate.test_db import (
    delete_database_tables,
    init_test_database,
)
from webapp_st_boilerplate.auth.login import change_password, login


def test_change_password():
    #: Init test database
    _, _ = init_test_database()

    #: Test change password
    (password_changed, response_str) = change_password(
        email="test.user@example.com",
        old_password="Password123!",  # noqa: S106
        new_password="NuovaPassword123!",  # noqa: S106
    )
    assert password_changed, "!!! Error in login !!!"
    assert response_str == "Password aggiornata", "!!! Error in login !!!"

    #: Test error in change_password
    (password_changed, response_str) = change_password(
        email="test.user@example.com",
        old_password="Password123!",  # noqa: S106
        new_password="NuovaPassword123!",  # noqa: S106
    )
    assert not password_changed, "!!! Error in login !!!"
    assert response_str == (
        "L'attuale password non è corretta. Non è stato possibile aggiornare la password"
    )

    #: Test error in change_password
    (password_changed, response_str) = change_password(
        email="test.user@example.com",
        old_password="NuovaPassword123!",  # noqa: S106
        new_password="newpsw",  # noqa: S106
    )
    assert not password_changed, "!!! Error in login !!!"

    #: Test error in change_password
    (password_changed, response_str) = change_password(
        email="test.user@example.com",
        old_password="NuovaPassword123!",  # noqa: S106
        new_password="newpswfdare",  # noqa: S106
    )
    assert not password_changed, "!!! Error in login !!!"

    #: Test error in change_password
    (password_changed, response_str) = change_password(
        email="wrongemail@example.com",
        old_password="NuovaPassword123!",  # noqa: S106
        new_password="newpswfdare",  # noqa: S106
    )
    assert not password_changed, "!!! Error in login !!!"

    #: Delete test database
    delete_database_tables()


def test_login():
    #: Init test database
    _, _ = init_test_database()

    (user_exist, wrong_password, _, _, _, _, _) = login(
        email="test.user@example.com",
        password="Password123!",  # noqa: S106
    )
    assert user_exist, "!!! Error in login !!!"
    assert wrong_password is False, "!!! Error in login !!!"

    #: Delete test database
    delete_database_tables()
