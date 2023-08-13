from constants import DEFAULT_API_RESPONSE_OBJ, RESPONSE_STATUS_KWD, RESPONSE_MSG_KWD
from management.task_assignments.operations import TaskAssignment, TaskAssignmentDB

def add_new_task_assignment(content):
    """This function will add new task to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to create task at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Adding new task to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD], _ = TaskAssignmentDB().add_task_assignment(
                task_id=content["task_id"],
                username=content["username"],
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully added Task assignment to DB: {content['name']}"

    except Exception as ex:
        print(f"Error Occured add_new_task_assignment - {ex}")
    return response

def update_task_assignment(content):
    """This function will update task assignment to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to update task assignment at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Updating task to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = TaskAssignmentDB().update_task_assignment(
                task_id=content["task_id"],
                username=content["username"],
            )
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully updated task assignment: {content['task_id']}"

    except Exception as ex:
        print(f"Error Occured update_task_assignment - {ex}")
    return response

def delete_task_assignment(content):
    """This function will delete task to our DB"""
    response = DEFAULT_API_RESPONSE_OBJ.copy()
    response[
        RESPONSE_MSG_KWD
    ] = "We are unable to delete task assignment at this moment. Please try again or contact MCube Tech Team."
    try:
        print(f"Deleting task assignment to DB: {content}")
        if content:
            response[RESPONSE_STATUS_KWD] = TaskAssignmentDB().delete_task_assignment(task_id=content["task_id"], username=content["username"])
            if response[RESPONSE_STATUS_KWD]:
                response[RESPONSE_MSG_KWD] = f"We have successfully deleted Task Assignment: {content['task_id']}"

    except Exception as ex:
        print(f"Error Occured delete_task_assignment - {ex}")
    return response
