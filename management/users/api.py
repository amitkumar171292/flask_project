from constants import DEFAULT_API_RESPONSE_OBJ, RESPONSE_STATUS_KWD, RESPONSE_MSG_KWD
from management.users.operations import User, UserDB

def add_new_user(content):
    """This function will add new user to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to create user at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Adding new user to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD], _ = UserDB().add_user(
                name=content["name"],
                phone_number=content["phone_number"],
                email=content["email"]
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = "We have successfully added User to DB"

    except Exception as ex:
        print(f"Error Occured create_batch - {ex}")
    return response

def fetch_all_users():
    """This function will fetch all user from our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to fetch user data at this moment. Please try again or contact MCube Tech Team."
    try:
        user_data = UserDB().get_all_users()
        if user_data:
            response["entity_data"] = user_data
            response[RESPONSE_STATUS_KWD] = True
            response[RESPONSE_MSG_KWD] = "We have fetch the data successfully"

    except Exception as ex:
        print(f"Error Occured create_batch - {ex}")
    return response