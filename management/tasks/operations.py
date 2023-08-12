import uuid
from datetime import datetime
import random
import sqlite3
from sqlite3 import OperationalError
from typing import List

class Task:
    """
    This class gives definition of Tasks Table
    task_id: Unique id of the task
    project_id: Unique id of the project
    name: Name of the task
    description: Description of the task
    status: Status of the Task (NOT_STARTED/IN_PROGRESS/COMPLETED)
    last_modified: Timestamp with timezone while making changes to the tasks 
    """

    def __init__(self, task_id, project_id, name, description, status, last_modified) -> None:
        self.task_id = task_id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
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
    def load(d: dict) -> "Task":
        """This function returns Class object from dictionary"""
        return Task(**d)

    @staticmethod
    def loads(d: str) -> "Task":
        """This function returns Class object from string"""
        d = json.loads(d)
        return Task(**d)


class TaskDB:
    """Task DB operations"""

    def __init__(self):
        pass

    def add_task(self, project_id, name, description, status):
        """Add new Task in the db"""
        try:
            response = False
            print(f"Adding {name} task details to DB")
            response, task = _add_task(
                project_id,
                name,
                description,
                status
            )
        except Exception:
            print(f"Critical error in add_task - {name} ")
            response, task = False, None
        return response, task
    
    def update_task(self, task_id, project_id, name, description, status):
        """Update Task object details in the db"""
        try:
            response = False
            print(f"Updating {task_id} task details to DB")
            response = _update_task(
                task_id,
                project_id,
                name,
                description,
                status
            )
        except Exception:
            print(f"Critical error in update_task - {task_id} ")
            response = False
        return response
    
    def get_task(self, task_id) -> Task:
        """Get Task object details from the db"""
        try:
            print(f"Fetching task details - {task_id}")
            task = None
            task: Task = _get_task(task_id)
        except Exception as ex:
            print(f"Critical error in get_task - {ex}")
        return task
    
    def get_limited_tasks(self, page_number, record_count) -> List[Task]:
        """Get limited Task object from the db or []"""
        try:
            response: List[Task] = []
            print("Getting limited tasks added till now")
            response: List[Task] = _get_limited_tasks(page_number, record_count) or []
            print(f"get_limited_tasks from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_limited_tasks")
            response = []
        return response
    
    def get_total_tasks(self):
        """Returns Total tasks or 0"""
        try:
            response: int = 0
            print("Getting total tasks")
            response: int = _get_total_tasks() or 0
            print(f"get_total_tasks from DB - {response}")
        except Exception:
            print("Critical error in get_total_tasks")
            response = 0
        return response

    def get_all_tasks(self) -> List[Task]:
        """Get all Task object from the db or []"""
        try:
            response: List[Task]= []
            print("Getting all tasks added till now")
            response: List[Task] = _get_all_tasks() or []
            print(f"get_all_tasks from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_all_tasks")
            response = []
        return response

    def delete_task(self, task_id):
        """Returns status of deletion of task"""
        try:
            response = False
            print("Deleting task using task_id")
            response = _delete_task(task_id)
            print(f"delete_task from DB -{response}")
        except Exception:
            print("Critical error in delete_task")
        return response

# region TasksDB

def _add_task(name, description):
    """This is a private function to add task"""
    try:
        print(f"Adding new task having task_id: {name}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            project_id=project_id,
            name=name,
            description=description,
            status=status,
            last_modified=last_modified
        )
        sql = "INSERT INTO tasks (task_id, project_id, name, description, status, last_modified) VALUES (:task_id, :project_id, :name, :description, :status, :last_modified)"

        cursor.execute(sql, task.dump())
        conn.commit()
        cursor.close()
        conn.close()
        print("Added task details to db")
        return True, task
    except OperationalError as ex:
        print("Error occurred in _add_task")
        raise ex

def _update_task(task_id, project_id, name, description, status):
    """This is a private function to update task"""
    try:
        print(f"Updating task having task_id: {task_id}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()

        sql = "UPDATE tasks SET project_id = ?, name = ?, description = ?, status = ?, last_modified = ? WHERE task_id = ?;"
        task_data = (project_id, name, description, status, last_modified, task_id)

        cursor.execute(sql, task_data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Updated task details to db")
        return True
    except OperationalError as ex:
        print("Error occurred in _update_task")
        raise ex

def _get_task(task_id):
    """This is a private function to get task"""
    try:
        print(f"Fetching task having task_id: {task_id}")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = "SELECT task_id, project_id, name, description, status, last_modified FROM tasks where task_id = %s;"
        data = (task_id,)
        cursor.execute(sql, data)
        result = cursor.fetchone()
        _result = []
        # to avoid error if result is empty
        _result = [Task.load(dict(row)) for row in result]

        cursor.close()
        conn.close()

        print("Fetch data from the Task Db")
        if len(_result) >= 1:
            return _result[0]
        else:
            return None
    except OperationalError as ex:
        print("Error occurred in _get_task")
        raise ex

def _get_all_tasks():
    """This is a private function to get task"""
    try:
        print("Fetching all tasks")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        select_query = "SELECT * FROM tasks;"
        cursor.execute(select_query,)
        result = cursor.fetchall()
        _result = []
        # to avoid error if result is empty
        _result = [Task.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _result
    except OperationalError as ex:
        print("Error occurred in _get_all_tasks")
        raise ex

def _get_total_tasks():
    """This is a private function to get total tasks"""
    try:
        print("Fetching total tasks")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        count_query = "SELECT count(1) FROM tasks;"

        cursor.execute(count_query)
        total_records = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        return total_records
    except OperationalError as ex:
        print("Error occurred in _get_total_tasks")
        raise ex

def _get_limited_tasks(page_number, record_count):
    """This is a private function to get limited tasks"""
    try:
        print("Fetching limited tasks")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        # Calculate the OFFSET value based on page_number and record_count
        offset = (page_number - 1) * record_count

        # Fetch records with LIMIT and OFFSET
        query = "SELECT * FROM tasks OFFSET %s LIMIT %s"

        cursor.execute(query, (offset, record_count,),)
        result = cursor.fetchall()
        _results = []
        # to avoid error if result is empty
        _results = [Task.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _results
    except OperationalError as ex:
        print("Error occurred in _get_total_tasks")
        raise ex

def _delete_task(task_id):
    """This is private function to delete task related details"""
    try:
        print(f"Running delete task details - {task_id}")
        response = False
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        sql = """DELETE from tasks WHERE task_id = ?;"""
        data = (task_id,)
        cursor.execute(sql, data)
        row_count = cursor.rowcount
        if row_count == 1:
            response = True
            conn.commit()
        cursor.close()
        conn.close()
        print(f"Deleted task details to DB - {task_id}")
        return response
    except OperationalError as ex:
        print("Error occurred in _delete_task")
        raise ex

# endregion