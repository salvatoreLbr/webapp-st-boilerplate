from datetime import datetime

import openpyxl
import pandas as pd

from sqlalchemy import inspect

from webapp_st_boilerplate.auth.authorization import Role
from webapp_st_boilerplate.config import settings
from webapp_st_boilerplate.db import schemas
from webapp_st_boilerplate.db.gateway import DBGateway
from webapp_st_boilerplate.db.models import (
    Entity,
    User,
)


class Cmd:
    def __init__(self, user_id: int, entity_id: int):
        self.user_id = user_id
        self.entity_id = entity_id
        self.db_gateway = DBGateway()

    def backup_db(self):
        # Lista delle classi del tuo modello
        MODEL_CLASSES = [
            Entity,
            User,
        ]

        # Crea un nuovo workbook di openpyxl
        workbook = openpyxl.Workbook()

        # Per ogni classe del modello
        for model_class in MODEL_CLASSES:
            # Ottieni il nome della tabella
            table_name = model_class.__tablename__

            # Crea un nuovo foglio con il nome della tabella
            worksheet = workbook.create_sheet(title=table_name)

            # Ottieni l'inspector di SQLAlchemy per la classe
            inspector = inspect(model_class)

            # Ottieni i nomi delle colonne
            columns = [column.name for column in inspector.columns]

            # Scrivi i nomi delle colonne nella prima riga (orizzontalmente)
            worksheet.append(columns)

        # Salva il file Excel
        output_filename = "database_schema.xlsx"
        workbook.save(output_filename)

        print(f"Il file '{output_filename}' è stato creato con successo.")

    def create_entity(self, entity_dict: dict) -> tuple[bool, str]:
        entity_create_obj = schemas.EntityCreate(entityName=entity_dict["entityName"])
        try:
            _ = self.db_gateway.create_entity(info=entity_create_obj)
            return True, "Entity creata con successo"
        except Exception as e:
            return False, f"Entity non creata a causa del seguente errore: {e.args[0]}"

    def create_user(self, user_dict: dict, entity_id: int | None = None) -> tuple[bool, str]:
        now_timestamp = datetime.now()
        user_create_obj = schemas.UserCreate(
            name=user_dict["name"],
            email=user_dict["email"],
            password=user_dict["password"],
            role=user_dict["role"],
            disabled=user_dict["disabled"],
            lastLogin=now_timestamp,
            createdDate=now_timestamp,
            updatedDate=now_timestamp,
        )
        try:
            entity_id = entity_id if entity_id is not None else self.entity_id
            _ = self.db_gateway.create_user(info=user_create_obj, entity_id=entity_id)
            return True, "Utente creato con successo"
        except Exception as e:
            return False, f"Utente non creato a causa del seguente errore: {e.args[0]}"

    def disable_user(self, user_id: int) -> tuple[bool, str]:
        #: Get user info
        user_df = self.db_gateway.get_user(filter={"id": f"=={user_id}"})
        user_dict = user_df.to_dict(orient="index")
        user_value = [user_value for user_value in user_dict.values()][0]
        user_value["createdDate"] = datetime.strptime(
            user_value["createdDate"], "%Y-%m-%d %H:%M:%S"
        )
        user_value["disabled"] = True
        user_update_obj = schemas.UserCreate(**user_value)
        try:
            self.db_gateway.update_user(info=user_update_obj, user_id=user_id)
            return True, "Utente disabilitato con successo"
        except Exception as e:
            return False, f"Utente non disabilitato a causa del seguente errore: {e.args[0]}"

    def get_entity(self) -> pd.DataFrame:
        return self.db_gateway.get_entity()

    def get_users(self) -> pd.DataFrame:
        return self.db_gateway.get_user()

    def init_database(self):
        #: Check if User table is empty
        user_df = self.db_gateway.get_user()
        if user_df.empty:
            #: Create ADMIN application
            user_dict = {
                "name": "Admin",
                "email": settings.app_secrets.admin_email,
                "password": settings.app_secrets.admin_psw,
                "role": Role.ADMIN.name,
                "disabled": False,
            }
            self.create_user(user_dict=user_dict)
        else:
            pass
