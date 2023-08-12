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
                response[RESPONSE_MSG_KWD] = f"We have successfully added User to DB: {content['username']}"

    except Exception as ex:
        print(f"Error Occured add_new_user - {ex}")
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
            response[RESPONSE_MSG_KWD] = "We have fetched the data successfully"

    except Exception as ex:
        print(f"Error Occured fetch_all_users - {ex}")
    return response

def update_user(content):
    """This function will update user to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to update user at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Updating user to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = UserDB().update_user(
                username=content["entity_unique_id"],
                name=content["name"],
                phone_number=content["phone_number"],
                email=content["email"]
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully updated User: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured update_user - {ex}")
    return response

def delete_user(content):
    """This function will delete user to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to delete user at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Deleting user to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = UserDB().delete_user(username=content["entity_unique_id"])
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully deleted User: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured delete_user - {ex}")
    return response