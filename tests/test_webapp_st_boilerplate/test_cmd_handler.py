import os

from pathlib import Path

import pandas as pd

from tests.test_webapp_st_boilerplate.test_db import (
    delete_database_tables,
    init_test_database,
)
from webapp_st_boilerplate.auth.authentication import verify_hash
from webapp_st_boilerplate.auth.authorization import Role
from webapp_st_boilerplate.cmd_handler import Cmd


def test_backup_db():
    #: Init test database
    userId, entityId = init_test_database()

    #: Set Cmd
    cmd_obj = Cmd(user_id=userId, entity_id=entityId)

    #: Test backup_db method
    cmd_obj.backup_db()
    cur_path = Path(os.getcwd())
    backup_path = cur_path.joinpath("database_schema.xlsx")
    assert backup_path.exists(), "!!! Error in backup_db !!!"

    #: Delete backup file test
    backup_path.unlink()

    #: Delete test database
    delete_database_tables()


def test_create_entity():
    #: Init test database
    userId, entityId = init_test_database()

    #: Set Cmd
    cmd_obj = Cmd(user_id=userId, entity_id=entityId)

    #: Test create_item method
    entity_dict = {
        "entityName": "Test",
    }
    created_flag, _ = cmd_obj.create_entity(entity_dict=entity_dict)
    assert created_flag, "!!! Error in create_entity !!!"

    #: Delete test database
    delete_database_tables()


def test_create_user():
    #: Init test database
    userId, entityId = init_test_database()

    #: Set Cmd
    cmd_obj = Cmd(user_id=userId, entity_id=entityId)

    #: Test create_user method
    user_dict = {
        "name": "Test User",
        "email": "test.user@example.com",
        "password": "Password123!",  # noqa: S106
        "role": Role.ADMIN.name,
        "disabled": False,
    }
    created_flag, response_str = cmd_obj.create_user(user_dict=user_dict)
    assert created_flag is False, "!!! Error in create_supplier !!!"
    assert "Email già registrata" in response_str, "!!! Error in create_supplier !!!"

    user_dict = {
        "name": "Test User",
        "email": "test.user1@example.com",
        "password": "Password123!",  # noqa: S106
        "role": Role.ADMIN.name,
        "disabled": False,
    }
    created_flag, response_str = cmd_obj.create_user(user_dict=user_dict)
    assert created_flag is False, "!!! Error in create_supplier !!!"
    assert "Nome già utilizzato" in response_str, "!!! Error in create_supplier !!!"

    user_dict = {
        "name": "other Test User",
        "email": "other.test.user@example.com",
        "password": "Password123!",  # noqa: S106
        "role": Role.USER.name,
        "disabled": False,
    }
    created_flag, _ = cmd_obj.create_user(user_dict=user_dict)
    assert created_flag, "!!! Error in create_supplier !!!"

    #: Delete test database
    delete_database_tables()


def test_disable_user():
    userId, entityId = init_test_database()
    cmd_obj = Cmd(user_id=userId, entity_id=entityId)
    users_df = cmd_obj.get_users()
    idx_user = users_df.apply(lambda x: verify_hash("test.user@example.com", x["email"]), axis=1)
    user_id = int(users_df.loc[idx_user, "id"].values[0])
    disabled_flag, _ = cmd_obj.disable_user(user_id=user_id)
    assert disabled_flag, "!!! Error in disable_user !!!"
    users_df = cmd_obj.get_users()
    idx_user = users_df.apply(lambda x: verify_hash("test.user@example.com", x["email"]), axis=1)
    user_row = users_df[idx_user]
    disabled = bool(user_row.iloc[0]["disabled"])
    assert not user_row.empty and disabled is True, (
        "!!! Error in disable_user: user not disabled !!!"
    )
    delete_database_tables()


def test_get_users():
    #: Init test database
    userId, entityId = init_test_database()

    #: Set Cmd
    cmd_obj = Cmd(user_id=userId, entity_id=entityId)

    #: Create user
    user_dict = {
        "name": "Test User 2",
        "email": "test.user2@example.com",
        "password": "Password123!",
        "role": Role.ADMIN.name,
        "disabled": False,
    }
    created_flag, _ = cmd_obj.create_user(user_dict=user_dict)
    assert created_flag, "!!! Error in create_user (setup) !!!"

    #: Test get_user method
    users_df = cmd_obj.get_users()
    assert isinstance(users_df, pd.DataFrame), "!!! Error in get_user: user not found !!!"
    idx_check = users_df["name"] == "Test User"
    assert idx_check.sum() > 0, "!!! Error in get_user: wrong user data !!!"

    #: Delete test database
    delete_database_tables()


def test_init_database():
    #: Set Cmd
    cmd_obj = Cmd(user_id=-9, entity_id=-9)

    #: Exec init database
    cmd_obj.init_database()

    #: Check admin presence
    users_df = cmd_obj.get_users()
    assert "Admin" in list(users_df["name"].unique()), "!!! Error in init_database"

    #: Delete test database
    delete_database_tables()
