from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from constants import TaskStatus
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, text
from db import DbConfig

app = Flask(__name__)

_ = DbConfig(app)

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
