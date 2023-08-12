from constants import DEFAULT_API_RESPONSE_OBJ

def add_new_user(content):
    """This function will add new user to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to create user at this moment. Please try again or contact MCube Tech Team."
    try:
        print(content)
    except Exception as ex:
        print(f"Error Occured create_batch - {ex}")
    return response