from datetime import datetime

from webapp_st_boilerplate.auth.authorization import Role
from webapp_st_boilerplate.db import models
from webapp_st_boilerplate.db.gateway import DBGateway
from webapp_st_boilerplate.db.main import get_db
from webapp_st_boilerplate.db.schemas import EntityCreate, UserCreate


def init_test_database() -> tuple[int, int]:
    """Function to create test database.

    Returns:
        int: userId created in database
    """
    #: Init test database
    db_gateway = DBGateway()

    #: Create entity
    entity_create_obj = EntityCreate(entityName="Test Entity")
    entity_id = db_gateway.create_entity(info=entity_create_obj)

    #: Create user
    user_to_create_obj = UserCreate(
        name="Test User",
        email="test.user@example.com",
        password="Password123!",  # noqa: S106
        role=Role.ADMIN.name,
        disabled=False,
        lastLogin=datetime.now(),
        createdDate=datetime.now(),
        updatedDate=datetime.now(),
    )
    user_id = db_gateway.create_user(info=user_to_create_obj, entity_id=entity_id)
    return user_id, entity_id


def delete_database_tables():
    db_session = get_db()
    for model in [
        models.Entity,
        models.Event,
        models.User,
    ]:
        db_session.query(model).delete(synchronize_session="evaluate")
    db_session.commit()
    db_session.expire_all()
    db_session.close()
