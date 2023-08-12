from constants import DEFAULT_API_RESPONSE_OBJ, RESPONSE_STATUS_KWD, RESPONSE_MSG_KWD
from management.tasks.operations import Task, TaskDB

def add_new_task(content):
    """This function will add new task to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to create task at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Adding new task to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD], _ = TaskDB().add_task(
                project_id=content["project_id"],
                name=content["name"],
                description=content["description"],
                status=content["status"]
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully added Task to DB: {content['task_id']}"

    except Exception as ex:
        print(f"Error Occured add_new_task - {ex}")
    return response

def fetch_all_tasks():
    """This function will fetch all task from our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to fetch task data at this moment. Please try again or contact MCube Tech Team."
    try:
        task_data = TaskDB().get_all_tasks()
        if task_data:
            response["entity_data"] = task_data
            response[RESPONSE_STATUS_KWD] = True
            response[RESPONSE_MSG_KWD] = "We have fetched the data successfully"

    except Exception as ex:
        print(f"Error Occured fetch_all_tasks - {ex}")
    return response

def update_task(content):
    """This function will update task to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to update task at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Updating task to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = TaskDB().update_task(
                task_id=content["entity_unique_id"],
                project_id=content["project_id"],
                name=content["name"],
                description=content["description"],
                status=content["status"]
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully updated task: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured update_task - {ex}")
    return response

def delete_task(content):
    """This function will delete task to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to delete task at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Deleting task to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = TaskDB().delete_task(task_id=content["entity_unique_id"])
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully deleted Task: {content['entity_unique_id']}"

    except Exception as ex:
        print(f"Error Occured delete_task - {ex}")
    return response