import uuid
from datetime import datetime
import random

class UsersDB:
    """Users DB operations"""

    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email

    def add_user(self, name, phone_number, email):
        """Add new user in the db"""
        try:
            response = False
            print(f"Adding {name} user details to DB")
            response = _add_user(
                name,
                phone_number,
                email,
            )
        except Exception:
            print(f"Critical error in add_user - {name} ")
            response = False
        return response
    
    def update_user(self, name, phone_number, email):
        """Update UserDB object details in the db"""
        try:
            response = False
            print(f"Updating {name} user details to DB")
            response = _update_user(
                name,
                phone_number,
                email,
            )
        except Exception:
            print(f"Critical error in update_user - {name} ")
            response = False
        return response
    
    def get_user(self, username):
        """Get UserDB object details from the db"""
        try:
            print(f"Fetching user details - {username}")
            user = None
            user: User = _get_user(username)
        except Exception as ex:
            print(f"Critical error in get_user - {ex}")
        return user
    
    def get_limited_users(self, page_number, record_count):
        """Get limited object from the db or []"""
        try:
            response = []
            print("Getting limited users added till now")
            response = _get_limited_users(page_number, record_count) or []
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

    def get_all_users(self):
        """Get all users object from the db or []"""
        try:
            response = []
            print("Getting all users added till now")
            response = _get_all_users() or []
            print(f"get_all_users from DB - {response}"[:5])
        except Exception:
            print("Critical error in get_all_users")
            response = []
        return response

# region UsersDB

def _add_user(name, phone_number, email):
    """This is a private function to add user"""
    try:
        print(f"Adding new user having username: {name}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()
        last_modified = datetime.utcnow()
        username = name.split(' ')[0] + str(random.randint(10000, 99999))

        insert_user = "INSERT INTO users (username, name, phone_number, email, last_modified) VALUES (?, ?, ?, ?, ?)"
        user_data = (username, name, phone_number, email, last_modified)

        cursor.execute(insert_user, user_data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
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

        update_user = "UPDATE users SET name = ?, phone_number = ?, email = ?, last_modified = ? WHERE username = ?;"
        user_data = (name, phone_number, email, last_modified, username)

        cursor.execute(update_user, user_data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except OperationalError as ex:
        print("Error occurred in _update_user")
        raise ex


def _get_user(username):
    """This is a private function to get user"""
    try:
        print(f"Fetching user having username: {username}")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        select_query = "SELECT username, name, phone_number, email, last_modified FROM users;"

        cursor.execute(select_query)
        result = cursor.fetchone()
        _result = None
        # to avoid error if result is empty
        for row in result:
            _result = dict(row)

        conn.commit()
        cursor.close()
        conn.close()
        return _result
    except OperationalError as ex:
        print("Error occurred in _get_user")
        raise ex

def _get_all_users():
    """This is a private function to get user"""
    try:
        print("Fetching user having username")
        conn = sqlite3.connect('mcube.db')
        cursor = conn.cursor()

        select_query = "SELECT * FROM users;"

        cursor.execute(select_query)
        result = cursor.fetchall()
        _result = []
        # to avoid error if result is empty
        for row in result:
            _result.append(dict(row))

        conn.commit()
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
        cursor = conn.cursor()

        # Calculate the OFFSET value based on page_number and record_count
        offset = (page_number - 1) * record_count

        # Fetch records with LIMIT and OFFSET
        query = f"SELECT * FROM users LIMIT {record_count} OFFSET {offset}"

        cursor.execute(query)
        result = cursor.fetchall()
        _results = []
        # to avoid error if result is empty
        for row in result:
            _results.append(dict(row))

        conn.commit()
        cursor.close()
        conn.close()
        return _results
    except OperationalError as ex:
        print("Error occurred in _get_total_users")
        raise ex

# endregion