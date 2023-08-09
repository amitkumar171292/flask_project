from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from constants import TaskStatus
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, text

app = Flask(__name__)

app.config['DATABASE'] = 'macube.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')


engine = create_engine('sqlite:///mcube.db')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<page_type>/")
def pages(page_type):
    if page_type in ["projects", "tasks", "users"]:
        # Declare your SQL query using text function
        query = text('SELECT * FROM users')
        # Execute the query using the engine
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        # Print the retrieved rows
        for row in rows:
            print(row)
        return render_template(page_type + "/index.html")
    else:
        return abort(404)
  
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


# Connect to a new or existing database (creates if not exists)
conn = sqlite3.connect('mcube.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Example INSERT statements for a 'users' table
insert_user = "INSERT INTO users (user_id, username, email) VALUES (?, ?, ?)"
user_data = (1, 'amitkumar', 'amitkumar@gmail.com')

# Execute the INSERT statement
cursor.execute(insert_user, user_data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
