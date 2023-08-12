from datetime import datetime
import random
import sqlite3
from sqlite3 import OperationalError
from typing import List

class User:
    """
    This class gives definition of Users Table
    username: Unique id of the user
    name: Name of the user
    phone_number: Phone number of the user
    email: Email of the user
    last_modified: Timestamp with timezone while making changes to the users 
    """

    def __init__(self, username, name, phone_number, email, last_modified) -> None:
        self.username = username
        self.name = name
        self.phone_number = phone_number
        self.email = email
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
    def load(d: dict) -> "User":
        """This function returns Class object from dictionary"""
        return User(**d)

    @staticmethod
    def loads(d: str) -> "User":
        """This function returns Class object from string"""
        d = json.loads(d)
        return User(**d)


class UserDB:
    """User DB operations"""

    def __init__(self):
        pass

    def add_user(self, name, phone_number, email):
        """Add new User in the db"""
        try:
            response = False
            print(f"Adding {name} user details to DB")
            response, user = _add_user(
                name,
                phone_number,
                email,
            )
        except Exception:
            print(f"Critical error in add_user - {name} ")
            response, user = False, None
        return response, user
    
    def update_user(self, username, name, phone_number, email):
        """Update User object details in the db"""
        try:
            response = False
            print(f"Updating {username} user details to DB")
            response = _update_user(
                username,
                name,
                phone_number,
                email,
            )
        except Exception:
            print(f"Critical error in update_user - {username} ")
            response = False
        return response
    
    def get_user(self, username) -> User:
        """Get User object details from the db"""
        try:
            print(f"Fetching user details - {username}")
            user = None
            user: User = _get_user(username)
        except Exception as ex:
            print(f"Critical error in get_user - {ex}")
        return user
    
    def get_limited_users(self, page_number, record_count) -> List[User]:
        """Get limited User object from the db or []"""
        try:
            response: List[User] = []
            print("Getting limited users added till now")
            response: List[User] = _get_limited_users(page_number, record_count) or []
            print(f"get_limited_users from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_limited_users")
            response = []
        return response
    
    def get_total_users(self):
        """Returns Total users or 0"""
        try:
            response: int = 0
            print("Getting total users")
            response: int = _get_total_users() or 0
            print(f"get_total_users from DB - {response}")
        except Exception:
            print("Critical error in get_total_users")
            response = 0
        return response

    def get_all_users(self) -> List[User]:
        """Get all User object from the db or []"""
        try:
            response: List[User]= []
            print("Getting all users added till now")
            response: List[User] = _get_all_users() or []
            print(f"get_all_users from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_all_users")
            response = []
        return response

    def delete_user(self, username):
        """Returns status of deletion of user"""
        try:
            response = False
            print("Deleting user using username")
            response = _delete_user(username)
            print(f"delete_user from DB -{response}")
        except Exception:
            print("Critical error in delete_user")
        return response

# region UsersDB

def _add_user(name, phone_number, email):
    """This is a private function to add user"""
    try:
        print(f"Adding new user having username: {name}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()
        username = name.split(' ')[0].lower() + str(random.randint(10000, 99999))
        user = User(
            username=username,
            name=name,
            phone_number=phone_number,
            email=email,
            last_modified=last_modified
        )
        sql = "INSERT INTO users (username, name, phone_number, email, last_modified) VALUES (:username, :name, :phone_number, :email, :last_modified);"

        cursor.execute(sql, user.dump())
        conn.commit()
        cursor.close()
        conn.close()
        print("Added user details to db")
        return True, user
    except OperationalError as ex:
        print("Error occurred in _add_user")
        raise ex

def _update_user(username, name, phone_number, email):
    """This is a private function to update user"""
    try:
        print(f"Updating user having username: {username}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()

        sql = "UPDATE users SET name = ?, phone_number = ?, email = ?, last_modified = ? WHERE username = ?;"
        user_data = (name, phone_number, email, last_modified, username)

        cursor.execute(sql, user_data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Updated user details to db")
        return True
    except OperationalError as ex:
        print("Error occurred in _update_user")
        raise ex

def _get_user(username):
    """This is a private function to get user"""
    try:
        print(f"Fetching user having username: {username}")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = "SELECT username, name, phone_number, email, last_modified FROM users where username = %s;"
        data = (username,)
        cursor.execute(sql, data)
        result = cursor.fetchone()
        _result = []
        # to avoid error if result is empty
        _result = [User.load(dict(row)) for row in result]

        cursor.close()
        conn.close()

        print("Fetch data from the User Db")
        if len(_result) >= 1:
            return _result[0]
        else:
            return None
    except OperationalError as ex:
        print("Error occurred in _get_user")
        raise ex

def _get_all_users():
    """This is a private function to get user"""
    try:
        print("Fetching all users")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        select_query = "SELECT * FROM users;"
        cursor.execute(select_query,)
        result = cursor.fetchall()
        _result = []
        # to avoid error if result is empty
        _result = [User.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _result
    except OperationalError as ex:
        print("Error occurred in _get_all_users")
        raise ex

def _get_total_users():
    """This is a private function to get total users"""
    try:
        print("Fetching total users")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        count_query = "SELECT count(1) FROM users;"

        cursor.execute(count_query)
        total_records = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        return total_records
    except OperationalError as ex:
        print("Error occurred in _get_total_users")
        raise ex

def _get_limited_users(page_number, record_count):
    """This is a private function to get limited users"""
    try:
        print("Fetching limited users")
        conn = sqlite3.connect('mcube.db')
        conn.row_factory = sqlite3.Row  # Set the Row factory
        cursor = conn.cursor()

        # Calculate the OFFSET value based on page_number and record_count
        offset = (page_number - 1) * record_count

        # Fetch records with LIMIT and OFFSET
        query = "SELECT * FROM users OFFSET %s LIMIT %s"

        cursor.execute(query, (offset, record_count,),)
        result = cursor.fetchall()
        _results = []
        # to avoid error if result is empty
        _results = [User.load(dict(row)) for row in result]

        cursor.close()
        conn.close()
        return _results
    except OperationalError as ex:
        print("Error occurred in _get_total_users")
        raise ex

def _delete_user(username):
    """This is private function to delete user related details"""
    try:
        print(f"Running delete user details - {username}")
        response = False
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        sql = """DELETE from users WHERE username = ?;"""
        data = (username,)
        cursor.execute(sql, data)
        row_count = cursor.rowcount
        if row_count == 1:
            response = True
            conn.commit()
        cursor.close()
        conn.close()
        print(f"Deleted user details to DB - {username}")
        return response
    except OperationalError as ex:
        print("Error occurred in _delete_user")
        raise ex

# endregion