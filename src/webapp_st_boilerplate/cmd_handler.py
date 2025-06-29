from datetime import datetime

import openpyxl
import pandas as pd

from sqlalchemy import inspect

from webapp_st_boilerplate.db import schemas
from webapp_st_boilerplate.db.gateway import DBGateway
from webapp_st_boilerplate.db.models import (
    Entity,
    Event,
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
            Event,
            User,
        ]

        # Crea un nuovo workbook di openpyxl
        workbook = openpyxl.Workbook()

        # Rimuovi il foglio di default creato all'apertura
        if "Sheet" in workbook.sheetnames:
            del workbook["Sheet"]

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

    def create_user(self, user_dict: dict) -> tuple[bool, str]:
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
            _ = self.db_gateway.create_user(info=user_create_obj, entity_id=self.entity_id)
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
            self.db_gateway.update_user(info=user_update_obj, user_id=self.user_id)
            return True, "Utente disabilitato con successo"
        except Exception as e:
            return False, f"Utente non disabilitato a causa del seguente errore: {e.args[0]}"

    def get_users(self) -> pd.DataFrame:
        return self.db_gateway.get_user()

    def update_user(self, user_dict: dict[str, str]) -> tuple[bool, str]:
        now_timestamp = datetime.now()
        user_dict["updatedDate"] = now_timestamp
        user_update_obj = schemas.UserCreate(**user_dict)
        try:
            self.db_gateway.update_user(info=user_update_obj, user_id=self.user_id)
            return True, "Utente aggiornato con successo"
        except Exception as e:
            return False, f"Utente non aggiornato a causa del seguente errore: {e.args[0]}"
