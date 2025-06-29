from datetime import datetime

import pandas as pd

from pydantic import BaseModel
from sqlalchemy.orm import Session

from webapp_st_boilerplate.db import models
from webapp_st_boilerplate.db.main import Base


##############
### Create ###
##############
def create_record(
    db_session: Session,
    model: Base,  # type: ignore
    info_list: list[models.Entity | models.Event | models.User],
) -> tuple[bool, str, list[int]]:
    try:
        db_session.add_all(info_list)
        db_session.commit()
        #: Get ID instance added
        id_list = [
            info_obj.id for info_obj in info_list if "History" not in info_obj.__tablename__
        ]
        db_session.flush(model)
        # Close session
        db_session.expire_all()
        # Close session
        db_session.close()
        print("Table updated!")
        return True, "ok", id_list
    except Exception as e:
        print(f"Eccezione: {e}")
        db_session.rollback()
        db_session.expire_all()
        db_session.close()
        print("Table NOT updated!")
        return False, e.__class__.__name__, []


######################
#### select funcs ####
######################
def get_record(
    db_session: Session,
    model: Base,  # type: ignore
    schema: BaseModel | None = None,
    filter: dict[str, str] | None = None,
):  # type: ignore
    #: Get table from db
    db_obj = db_session.query(model).all()
    #: Get fields name of model
    fields_name = []
    for key, value in model.__dict__.items():
        try:
            if (value.is_attribute) & (key[0] != "_") & ("link" not in key):
                fields_name.append(key)
        except Exception:
            pass
    #: Get row values
    db_list = []
    for db_row in db_obj:
        row_dict = {}
        for key in fields_name:
            try:
                value = getattr(db_row, key)
                row_dict[key] = value
            except Exception:
                pass
        db_list.append(row_dict)
    #: Transform obj db in pd.DataFrame
    if schema is not None:
        df = pd.DataFrame([schema(**row).__dict__ for row in db_list])
    else:
        df = pd.DataFrame(data=db_list, columns=fields_name)
    # Close session
    db_session.expire_all()
    db_session.close()
    #: Drop _sa_instance_state field if exists
    if "_sa_instance_state" in df.columns:
        df = df.drop(["_sa_instance_state"], axis=1)
    #: Filter if any
    if (filter is not None) & (not df.empty):
        idx_filter = []
        for key, value in filter.items():
            idx_filter.append(f"(df.{key}{value}) &")
        idx_filter = "".join(idx_filter)
        idx_filter = idx_filter[:-2]
        df = df.loc[eval(idx_filter)].reset_index(drop=True)
    return df


######################
#### update funcs ####
######################
def update_record(
    db_session: Session,
    model: Base,  # type: ignore
    filter_criteria: list[tuple[str, int | float | str | datetime]],
    updates: dict[str, int | float | str | datetime],
) -> None:
    """
    Updates an existing record in a table specified by the model.

    Args:
        db (Session): The SQLAlchemy database session.
        model (Base): The SQLAlchemy model class of the table to update.
        record_id (int): The ID of the record to update.
        updates (Dict[str, Any]): A dictionary where keys are the attribute names of the model
                                   (e.g., 'name', 'email', 'quantity') and values are the new data.

    Returns:
        Any | None: The updated object if found, otherwise None.
    """
    #: Get actual record
    query = db_session.query(model)

    #: Filter table
    for field_name, field_value in filter_criteria:
        if hasattr(model, field_name):
            query = query.filter(getattr(model, field_name) == field_value)
        else:
            pass
    record = query.first()

    if record is None:
        print("No record found for the given filters")
    else:
        #: Update attributes
        for key, value in updates.items():
            # Utilizza setattr per impostare dinamicamente gli attributi dell'oggetto
            # Questo invocherà automaticamente i setter delle @hybrid_property se presenti
            setattr(record, key, value)

        #: Commit
        try:
            db_session.commit()
            print("Record updated!")
            # Close session
            db_session.expire_all()
            # Close session
            db_session.close()
        except Exception as e:
            db_session.rollback()
            db_session.expire_all()
            db_session.close()
            print(f"Update error with following error: {e}")


######################
#### delete funcs ####
######################
def delete_record(
    db_session: Session,
    model: Base,  # type: ignore
    filter: dict[str, str] | None = None,
):  # type: ignore
    #: Remove records from table's DB
    if filter is not None:
        idx_filter = []
        for key, value in filter.items():
            idx_filter.append(f"(model.{key}{value}) &")
        idx_filter = "".join(idx_filter)
        idx_filter = idx_filter[:-2]
        db_session.query(model).filter(eval(idx_filter)).delete(synchronize_session="evaluate")
    else:
        db_session.query(model).delete(synchronize_session="evaluate")
    #: Update DB
    db_session.commit()
    db_session.expire_all()
    db_session.close()
