import uuid
from datetime import datetime
import random
import sqlite3
from sqlite3 import OperationalError
from typing import List

class Project:
    """
    This class gives definition of Projects Table
    project_id: Unique id of the project
    name: Name of the project
    description: Description of the project
    last_modified: Timestamp with timezone while making changes to the projects 
    """

    def __init__(self, project_id, name, description, last_modified) -> None:
        self.project_id = project_id
        self.name = name
        self.description = description
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
    def load(d: dict) -> "Project":
        """This function returns Class object from dictionary"""
        return Project(**d)

    @staticmethod
    def loads(d: str) -> "Project":
        """This function returns Class object from string"""
        d = json.loads(d)
        return Project(**d)


class ProjectDB:
    """Project DB operations"""

    def __init__(self):
        pass

    def add_project(self, name, description):
        """Add new Project in the db"""
        try:
            response = False
            print(f"Adding {name} project details to DB")
            response, project = _add_project(
                name,
                description
            )
        except Exception:
            print(f"Critical error in add_project - {name} ")
            response, project = False, None
        return response, project
    
    def update_project(self, project_id, name, description):
        """Update Project object details in the db"""
        try:
            response = False
            print(f"Updating {project_id} project details to DB")
            response = _update_project(
                project_id,
                name,
                description
            )
        except Exception:
            print(f"Critical error in update_project - {project_id} ")
            response = False
        return response
    
    def get_project(self, project_id) -> Project:
        """Get Project object details from the db"""
        try:
            print(f"Fetching project details - {project_id}")
            project = None
            project: Project = _get_project(project_id)
        except Exception as ex:
            print(f"Critical error in get_project - {ex}")
        return project
    
    def get_limited_projects(self, page_number, record_count) -> List[Project]:
        """Get limited Project object from the db or []"""
        try:
            response: List[Project] = []
            print("Getting limited projects added till now")
            response: List[Project] = _get_limited_projects(page_number, record_count) or []
            print(f"get_limited_projects from DB - {response}")
        except Exception:
            print("Critical error in get_limited_projects")
            response = []
        return response
    
    def get_total_projects(self):
        """Returns Total projects or 0"""
        try:
            response: int = 0
            print("Getting total projects")
            response: int = _get_total_projects() or 0
            print(f"get_total_projects from DB - {response}")
        except Exception:
            print("Critical error in get_total_projects")
            response = 0
        return response

    def get_all_projects(self) -> List[Project]:
        """Get all Project object from the db or []"""
        try:
            response: List[Project]= []
            print("Getting all projects added till now")
            response: List[Project] = _get_all_projects() or []
            print(f"get_all_projects from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_all_projects")
            response = []
        return response

    def delete_project(self, project_id):
        """Returns status of deletion of project"""
        try:
            response = False
            print("Deleting project using project_id")
            response = _delete_project(project_id)
            print(f"delete_project from DB -{response}")
        except Exception:
            print("Critical error in delete_project")
        return response

# region ProjectsDB

def _add_project(name, description):
    """This is a private function to add project"""
    try:
        print(f"Adding new project having project_id: {name}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()
        project_id = str(uuid.uuid4())
        project = Project(
            project_id=project_id,
            name=name,
            description=description,
            last_modified=last_modified
        )
        sql = "INSERT INTO projects (project_id, name, description, last_modified) VALUES (:project_id, :name, :description, :last_modified);"

        print
        cursor.execute(sql, project.dump())
        conn.commit()
        cursor.close()
        conn.close()
        print("Added project details to db")
        return True, project
    except OperationalError as ex:
        print("Error occurred in _add_project")
        raise ex

def _update_project(project_id, name, description):
    """This is a private function to update project"""
    try:
        print(f"Updating project having project_id: {project_id}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()

        sql = "UPDATE projects SET name = ?, description = ?, last_modified = ? WHERE project_id = ?;"
        project_data = (name, description, last_modified, project_id)

        cursor.execute(sql, project_data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Updated project details to db")
        return True
    except OperationalError as ex:
        print("Error occurred in _update_project")
        raise ex

def _get_project(project_id):
    """This is a private function to get project"""
    try:
        print(f"Fetching project having project_id: {project_id}")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = "SELECT project_id, name, description, last_modified FROM projects where project_id = ?;"
        data = (project_id,)
        cursor.execute(sql, data)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        print("Fetch data from the Project Db")
        if result is not None:
            return Project.load(dict(result))
        else:
            return None
    except OperationalError as ex:
        print("Error occurred in _get_project")
        raise ex

def _get_all_projects():
    """This is a private function to get project"""
    try:
        print("Fetching all projects")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        select_query = "SELECT * FROM projects;"
        cursor.execute(select_query,)
        result = cursor.fetchall()
        _result = []
        # to avoid error if result is empty
        _result = [Project.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _result
    except OperationalError as ex:
        print("Error occurred in _get_all_projects")
        raise ex

def _get_total_projects():
    """This is a private function to get total projects"""
    try:
        print("Fetching total projects")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        count_query = "SELECT count(1) FROM projects;"

        cursor.execute(count_query)
        total_records = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        return total_records
    except OperationalError as ex:
        print("Error occurred in _get_total_projects")
        raise ex

def _get_limited_projects(page_number, record_count):
    """This is a private function to get limited projects"""
    try:
        print("Fetching limited projects")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        # Calculate the OFFSET value based on page_number and record_count
        offset = (page_number - 1) * record_count

        # Fetch records with LIMIT and OFFSET
        query = "SELECT project_id, name, description, last_modified FROM projects LIMIT ? OFFSET ?;"

        cursor.execute(query, (record_count, offset))
        result = cursor.fetchall()
        print(result)
        _results = []
        # to avoid error if result is empty
        _results = [Project.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _results
    except OperationalError as ex:
        print("Error occurred in _get_limited_projects")
        raise ex

def _delete_project(project_id):
    """This is private function to delete project related details"""
    try:
        print(f"Running delete project details - {project_id}")
        response = False
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        sql = """DELETE from projects WHERE project_id = ?;"""
        data = (project_id,)
        cursor.execute(sql, data)
        row_count = cursor.rowcount
        if row_count == 1:
            response = True
            conn.commit()
        cursor.close()
        conn.close()
        print(f"Deleted project details to DB - {project_id}")
        return response
    except OperationalError as ex:
        print("Error occurred in _delete_project")
        raise ex

# endregion