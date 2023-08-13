from datetime import datetime
import sqlite3
from sqlite3 import OperationalError
from typing import List

class TaskAssignment:
    """
    This class gives definition of TaskAssignment Table
    task_id: Unique id of the task
    username: Unique id of the user
    last_modified: Timestamp with timezone while making changes to the task assignments 
    """

    def __init__(self, task_id, username, last_modified) -> None:
        self.task_id = task_id
        self.username = username
        self.last_modified = last_modified
    
    def dump(self) -> dict:
        """This function returns dictionary from Class object"""
        # Vars is being used to convert the data into dictionary by mapping column name with the value
        return dict(vars(self).items())

    def dumps(self) -> str:
        """This function returns string from Class object"""
        data = dict(vars(self).items())
        return json.dumps(data)

    @staticmethod
    def load(d: dict) -> "TaskAssignment":
        """This function returns Class object from dictionary"""
        return TaskAssignment(**d)

    @staticmethod
    def loads(d: str) -> "TaskAssignment":
        """This function returns Class object from string"""
        d = json.loads(d)
        return TaskAssignment(**d)


class TaskAssignmentDB:
    """TaskAssignment DB operations"""

    def __init__(self):
        pass

    def add_task_assignment(self, task_id, username):
        """Add new TaskAssignment in the db"""
        try:
            response = False
            print(f"Adding {task_id} task assignment details to DB")
            response, task_assignment = _add_task_assignment(
                task_id,
                username,
            )
        except Exception:
            print(f"Critical error in add_task_assignment - {task_id} ")
            response, task_assignment = False, None
        return response, task_assignment
    
    def update_task_assignment(self, task_id, username):
        """Update TaskAssignment object details in the db"""
        try:
            response = False
            print(f"Updating {task_id} task assignment details to DB")
            response = _update_task_assignment(
                task_id,
                username
            )
        except Exception:
            print(f"Critical error in update_task_assignment - {task_id} ")
            response = False
        return response
    
    def get_task_assignment(self, task_id, username) -> TaskAssignment:
        """Get TaskAssignment object details from the db"""
        try:
            print(f"Fetching task details - {task_id, username}")
            task_assignment = None
            task_assignment: TaskAssignment = _get_task_assignment(task_id, username)
        except Exception as ex:
            print(f"Critical error in get_task_assignment - {ex}")
        return task_assignment
    
    def get_limited_task_assignments(self, page_number, record_count) -> List[TaskAssignment]:
        """Get limited TaskAssignment object from the db or []"""
        try:
            response: List[TaskAssignment] = []
            print("Getting limited task assignments added till now")
            response: List[TaskAssignment] = _get_limited_task_assignments(page_number, record_count) or []
            print(f"get_limited_task_assignments from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_limited_task_assignments")
            response = []
        return response
    
    def get_total_task_assignments(self):
        """Returns Total task assignments or 0"""
        try:
            response: int = 0
            print("Getting total task assignments")
            response: int = _get_total_task_assignments() or 0
            print(f"get_total_task_assignments from DB - {response}")
        except Exception:
            print("Critical error in get_total_task_assignments")
            response = 0
        return response

    def get_all_task_assignments(self) -> List[TaskAssignment]:
        """Get all TaskAssignment object from the db or []"""
        try:
            response: List[TaskAssignment]= []
            print("Getting all task assignments added till now")
            response: List[TaskAssignment] = _get_all_task_assignments() or []
            print(f"get_all_task_assignments from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_all_task_assignments")
            response = []
        return response

    def delete_task_assignment(self, task_id, username):
        """Returns status of deletion of task"""
        try:
            response = False
            print("Deleting task using task_id")
            response = _delete_task_assignment(task_id, username)
            print(f"delete_task_assignment from DB -{response}")
        except Exception:
            print("Critical error in delete_task_assignment")
        return response

# region TasksDB

def _add_task_assignment(task_id, username):
    """This is a private function to add task assignment"""
    try:
        print(f"Adding task assignment having task_id: {task_id}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()
        task_asssignment = TaskAssignment(
            task_id=task_id,
            username=username,
            last_modified=last_modified
        )
        sql = "INSERT INTO task_assignments (task_id, username, last_modified) VALUES (:task_id, :username, :last_modified);"
        print(task_asssignment.dump())
        print(sql)
        cursor.execute(sql, task_asssignment.dump())
        conn.commit()
        cursor.close()
        conn.close()
        print("Added task asssignment details to db")
        return True, task_asssignment
    except OperationalError as ex:
        print("Error occurred in _add_task_assignment")
        raise ex

def _update_task_assignment(task_id, username):
    """This is a private function to update task assignment"""
    try:
        print(f"Updating task assignment having task_id: {task_id}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()

        sql = "UPDATE task_assignments SET task_id = ?, username = ?, last_modified = ? WHERE task_id = ? and username = ?;"
        task_data = (task_id, username, last_modified, task_id, username)

        cursor.execute(sql, task_data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Updated task assignment details to db")
        return True
    except OperationalError as ex:
        print("Error occurred in _update_task_assignment")
        raise ex

def _get_task_assignment(task_id, username):
    """This is a private function to get task assignment"""
    try:
        print(f"Fetching task assignment having task_id: {task_id}")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = "SELECT task_id, username, last_modified FROM task_assignments where task_id = ? and username = ?;"
        data = (task_id, username)
        cursor.execute(sql, data)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        print("Fetch data from the TaskAssignment Db")
        if result is not None:
            return TaskAssignment.load(dict(result))
        else:
            return None
    except OperationalError as ex:
        print("Error occurred in _get_task_assignment")
        raise ex

def _get_all_task_assignments():
    """This is a private function to get task assignment"""
    try:
        print("Fetching all task assignments")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        select_query = "SELECT * FROM task_assignments;"
        cursor.execute(select_query,)
        result = cursor.fetchall()
        _result = []
        # to avoid error if result is empty
        _result = [TaskAssignment.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _result
    except OperationalError as ex:
        print("Error occurred in _get_all_task_assignments")
        raise ex

def _get_total_task_assignments():
    """This is a private function to get total task assignments"""
    try:
        print("Fetching total task assignments")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        count_query = "SELECT count(1) FROM task_assignments;"

        cursor.execute(count_query)
        total_records = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        return total_records
    except OperationalError as ex:
        print("Error occurred in _get_total_task_assignments")
        raise ex

def _get_limited_task_assignments(page_number, record_count):
    """This is a private function to get limited task assignments"""
    try:
        print("Fetching limited task assignments")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        # Calculate the OFFSET value based on page_number and record_count
        offset = (page_number - 1) * record_count

        # Fetch records with LIMIT and OFFSET
        query = "SELECT * FROM task_assignments OFFSET ? LIMIT ?"

        cursor.execute(query, (offset, record_count))
        result = cursor.fetchall()
        _results = []
        # to avoid error if result is empty
        _results = [TaskAssignment.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _results
    except OperationalError as ex:
        print("Error occurred in _get_total_task_assignments")
        raise ex

def _delete_task_assignment(task_id, username):
    """This is private function to delete task related details"""
    try:
        print(f"Running delete task details - {task_id}")
        response = False
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        sql = """DELETE from task_assignments WHERE task_id = ? and username = ?;"""
        data = (task_id, username,)
        cursor.execute(sql, data)
        row_count = cursor.rowcount
        if row_count == 1:
            response = True
            conn.commit()
        cursor.close()
        conn.close()
        print(f"Deleted task assignment details to DB - {task_id}")
        return response
    except OperationalError as ex:
        print("Error occurred in _delete_task_assignment")
        raise ex

# endregion