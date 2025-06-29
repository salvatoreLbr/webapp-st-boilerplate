from datetime import datetime

import pytest

from tests.test_webapp_st_boilerplate.test_db import (
    delete_database_tables,
    init_test_database,
)
from webapp_st_boilerplate.auth.authorization import Role
from webapp_st_boilerplate.db import schemas
from webapp_st_boilerplate.db.gateway import DBGateway


def test_create_user():
    #: Init test database
    _, _ = init_test_database()

    #: Create new customer
    db_gateway = DBGateway()
    user_to_create_obj = schemas.UserCreate(
        name="Test User",
        email="test.user@example.com",
        password="Password123!",  # noqa: S106
        role=Role.ADMIN.name,
        disabled=False,
        lastLogin=datetime.now(),
        createdDate=datetime.now(),
        updatedDate=datetime.now(),
    )
    with pytest.raises(Exception) as e:
        db_gateway.create_user(info=user_to_create_obj, entity_id=0)
    assert e.value.args[0] == "Email già registrata", "Error in create_user"
    user_to_create_obj = schemas.UserCreate(
        name="Test User2",
        email="test.user2@example.com",
        password="password123!",  # noqa: S106
        role=Role.ADMIN.name,
        disabled=False,
        lastLogin=datetime.now(),
        createdDate=datetime.now(),
        updatedDate=datetime.now(),
    )
    with pytest.raises(Exception) as e:
        db_gateway.create_user(info=user_to_create_obj, entity_id=0)
    assert "Password non valida" in e.value.args[0], "Error in create_user"

    #: Delete test database
    delete_database_tables()


def test_get_user():
    #: Init test database
    userId, _ = init_test_database()

    #: Create new user
    db_gateway = DBGateway()
    entity_df = db_gateway.get_entity()
    user_to_create_obj = schemas.UserCreate(
        name="Test User 2",
        email="test.user2@example.com",
        password="!Password123",  # noqa: S106
        role=Role.USER.name,
        disabled=False,
    )
    db_gateway.create_user(info=user_to_create_obj, entity_id=int(entity_df.id.unique()[0]))
    all_user_df = db_gateway.get_user()
    filtered_df = db_gateway.get_user(filter={"id": f"=={userId}"})
    assert all_user_df.shape[0] > filtered_df.shape[0], "!!! Error in get_user with filter !!!"
    assert filtered_df.shape[0] == 1, "!!! Error in get_user with filter !!!"

    #: Delete test database
    delete_database_tables()


def test_update_user():
    userId, _ = init_test_database()
    db_gateway = DBGateway()
    filtered_df = db_gateway.get_user(filter={"id": f"=={userId}"})
    createdDate_str = filtered_df["createdDate"].values[0]
    createdDate_dt = datetime.strptime(createdDate_str, "%Y-%m-%d %H:%M:%S")

    #: Change name
    user_obj = schemas.UserCreate(
        name="User di prova",
        email="test.user@example.com",
        password="Password123!",  # noqa: S106
        role=Role.ADMIN.name,
        disabled=False,
        createdDate=createdDate_dt,
    )
    db_gateway.update_user(info=user_obj, user_id=userId)

    #: Check new name
    filtered_df = db_gateway.get_user(filter={"id": f"=={userId}"})
    assert "User di prova" in filtered_df["name"].values, "!!! Error in update_user !!!"

    #: Delete database tables
    delete_database_tables()
