from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from webapp_st_boilerplate.auth.authentication import check_rules_password, get_hash, verify_hash
from webapp_st_boilerplate.db import models, schemas
from webapp_st_boilerplate.db.crud import create_record, get_record, update_record
from webapp_st_boilerplate.db.main import Base, get_db


class Gateway(ABC):
    @abstractmethod
    def create_entity(self, info: schemas.EntityCreate) -> int: ...

    @abstractmethod
    def create_event(self, user_id: int, event_type: str, event_date: datetime) -> int: ...

    @abstractmethod
    def create_user(self, info: schemas.UserCreate, entity_id: int) -> int: ...

    @abstractmethod
    def get_entity(self, filter: dict[str, str] | None = None) -> pd.DataFrame: ...

    @abstractmethod
    def get_entity_id(self, user_id: int) -> int: ...

    @abstractmethod
    def get_event(self) -> pd.DataFrame: ...

    @abstractmethod
    def get_user(self, filter: dict[str, str] | None = None) -> pd.DataFrame: ...

    @abstractmethod
    def update_user(self, info: schemas.UserCreate, user_id: int) -> None: ...


class DBGateway(Gateway):
    def __init__(self) -> None:
        super().__init__()

    def _write_table(
        self,
        model: Base,  # type: ignore
        info: list[models.Entity | models.Event | models.User],
    ) -> list[int]:
        session = get_db()
        created, msg, id_list = create_record(db_session=session, model=model, info_list=info)
        if not created:
            raise Exception(msg)
        return id_list

    def create_entity(self, info: schemas.EntityCreate) -> int:
        """Create new entity in Entity table.

        Args:
            info (schemas.EntityCreate): new entity infos.

        Returns:
            int: ID of the newly created record in the Entity table.
        """
        entity_obj = models.Entity(entityName=info.entityName)
        entity_id_list = self._write_table(model=models.Entity, info=[entity_obj])
        return entity_id_list[0]

    def create_event(self, user_id: int, event_type: str, event_date: datetime) -> int:
        """
        Creates a new record in the Event table.

        Args:
            user_id (int): ID of the user who generated the event.
            event_type (str): Type of event (e.g., 'ADD', 'UPDATE', 'DELETE', etc.).
            event_date (datetime): Date and time when the event occurred.

        Returns:
            int: ID of the newly created record in the Event table.
        """
        #: Get entityId based on userId
        entity_id = self.get_entity_id(user_id=user_id)
        #: Create event
        event_obj = models.Event(
            userId=user_id,
            eventType=event_type,
            eventDate=event_date,
            entityId=entity_id,
        )
        event_id_list = self._write_table(model=models.Event, info=[event_obj])
        return event_id_list[0]

    def create_user(self, info: schemas.UserCreate, entity_id: int) -> int:
        """Create new user in User table.

        Args:
            info (schemas.UserCreate): new User's info
            entity_id (int): ID of the entity to which user belong to.

        Returns:
            int: ID of the new user
        """
        #: Check if user already exists
        user_df = self.get_user()
        if not user_df.empty:
            idx_df = user_df["email"].apply(lambda x: verify_hash(info.email, x))
            user_df = user_df.loc[idx_df].reset_index(drop=True)
        if user_df.empty:
            #: Check psw rules
            error_in_psw, type_response = check_rules_password(psw=info.password)
            if error_in_psw:
                raise Exception(f"Password non valida per la seguente ragione: {type_response}")
            now_timestamp = datetime.now()
            user_obj = models.User(
                entityId=entity_id,
                name=info.name,
                email=get_hash(info.email),
                password=get_hash(info.password),
                role=info.role,
                disabled=info.disabled,
                lastLogin=now_timestamp,
                createdDate=now_timestamp,
                updatedDate=now_timestamp,
            )
            user_id_list = self._write_table(model=models.User, info=[user_obj])
            return user_id_list[0]
        else:
            raise Exception("Email già registrata")

    def get_entity(self, filter: dict[str, str] | None = None) -> pd.DataFrame:
        entity_df = get_record(
            db_session=get_db(),
            model=models.Entity,
            filter=filter,
        )
        return entity_df

    def get_entity_id(self, user_id: int) -> int:
        entity_df = self.get_user(filter={"id": "==" + str(user_id)})
        return int(entity_df["entityId"].unique()[0])

    def get_event(self) -> pd.DataFrame:
        event_df = get_record(
            db_session=get_db(),
            model=models.Event,
        )
        return event_df

    def get_user(self, filter: dict[str, str] | None = None) -> pd.DataFrame:
        user_df = get_record(
            db_session=get_db(), model=models.User, schema=schemas.UserPandas, filter=filter
        )
        return user_df

    def update_user(self, info: schemas.UserCreate, user_id: int):
        """Function used to update user info except password.

        Args:
            info (schemas.UserCreate): _description_
            user_id (int): _description_
        """
        #: Get entityId based on userId
        entity_id = self.get_entity_id(user_id=user_id)
        #: Set now_timestamp
        now_timestamp = datetime.now()
        #: Update record
        user_dict = {
            "entityId": entity_id,
            "name": info.name,
            "email": info.email,
            "password": info.password,
            "role": info.role,
            "disabled": info.disabled,
            "lastLogin": now_timestamp,
            "createdDate": info.createdDate,
            "updatedDate": now_timestamp,
        }
        update_record(
            db_session=get_db(),
            model=models.User,
            filter_criteria=[("id", user_id)],
            updates=user_dict,
        )
