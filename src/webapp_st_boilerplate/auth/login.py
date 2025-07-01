from datetime import datetime

from webapp_st_boilerplate.auth.authentication import authenticate, check_rules_password, get_hash
from webapp_st_boilerplate.db.gateway import DBGateway
from webapp_st_boilerplate.db.schemas import UserCreate


def change_password(email: str, old_password: str, new_password: str) -> tuple[bool, str]:
    #: Set db_gateway
    db_gateway = DBGateway()

    #: Get users dataframe
    users_df = db_gateway.get_user()
    #: Authenticate
    (correct_email, wrong_password, _, _, _, user_id, _) = authenticate(
        users_df=users_df, email=email, password=old_password
    )
    if not correct_email:
        return (
            False,
            "L'email inserita non corrisponde a quella associata all'account",
        )
    elif wrong_password:
        return (
            False,
            "L'attuale password non è corretta. Non è stato possibile aggiornare la password",
        )
    else:
        error_in_psw, response_check = check_rules_password(psw=new_password)
        if error_in_psw:
            return False, f"La nuova password non rispetta i seguenti requisiti: {response_check}"
        else:
            #: Update password in database
            user_dict = users_df.loc[users_df["id"] == user_id].to_dict(orient="index")
            user_value = [user_value for user_value in user_dict.values()][0]
            user_value["password"] = get_hash(new_password)
            user_value["createdDate"] = datetime.strptime(
                user_value["createdDate"], "%Y-%m-%d %H:%M:%S"
            )
            user_obj = UserCreate(**user_value)
            db_gateway.update_user(info=user_obj, user_id=user_id)
            return True, "Password aggiornata"


def login(email: str, password: str) -> tuple[bool, bool, bool, int, str, int, int]:
    #: Set db_gateway
    db_gateway = DBGateway()

    #: Get users dataframe
    users_df = db_gateway.get_user()
    #: Authenticate
    (user_exist, wrong_password, disabled, role_number, name, user_id, entity_id) = authenticate(
        users_df=users_df, email=email, password=password
    )
    #: At this point login is ok
    if user_id != -9:
        #: Update last login
        user_dict = users_df.loc[users_df["id"] == user_id].to_dict(orient="index")
        user_value = [user_value for user_value in user_dict.values()][0]
        user_value["createdDate"] = datetime.strptime(
            user_value["createdDate"], "%Y-%m-%d %H:%M:%S"
        )
        user_obj = UserCreate(**user_value)
        db_gateway.update_user(info=user_obj, user_id=user_id)
    else:
        pass

    return user_exist, wrong_password, disabled, role_number, name, user_id, entity_id
