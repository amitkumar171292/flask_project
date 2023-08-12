from constants import DEFAULT_API_RESPONSE_OBJ, RESPONSE_STATUS_KWD, RESPONSE_MSG_KWD
from management.projects.operations import Project, ProjectDB

def add_new_project(content):
    """This function will add new project to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to create project at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Adding new project to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD], _ = ProjectDB().add_project(
                name=content["name"],
                description=content["description"],
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully added Project to DB: {content['name']}"

    except Exception as ex:
        print(f"Error Occured add_new_project - {ex}")
    return response

def fetch_all_projects():
    """This function will fetch all project from our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to fetch project data at this moment. Please try again or contact MCube Tech Team."
    try:
        project_data = ProjectDB().get_all_projects()
        if project_data:
            response["entity_data"] = project_data
            response[RESPONSE_STATUS_KWD] = True
            response[RESPONSE_MSG_KWD] = "We have fetched the data successfully"

    except Exception as ex:
        print(f"Error Occured fetch_all_projects - {ex}")
    return response

def update_project(content):
    """This function will update project to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to update project at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Updating project to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = ProjectDB().update_project(
                project_id=content["entity_unique_id"],
                name=content["name"],
                description=content["description"],
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully updated Project: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured update_project - {ex}")
    return response

def delete_project(content):
    """This function will delete project to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to delete project at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Deleting project to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = ProjectDB().delete_project(project_id=content["entity_unique_id"])
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully deleted Project: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured delete_project - {ex}")
    return response