from flask import Flask, render_template, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from constants import TaskStatus
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, text
from db import DbConfig
from management.users.operations import User, UserDB
from management.users.api import fetch_all_users, add_new_user
import requests
import json

app = Flask(__name__)

_ = DbConfig(app)

engine = create_engine('sqlite:///mcube.db')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<page_type>/")
def pages(page_type):
    if page_type in ["projects", "tasks", "users"]:
        resp = UserDB().add_user('Amit', 8744826266, 'amit.kumar@wizklub.com')
        if resp:
            response = UserDB().get_all_users()
            if response:
                print(response)

        return render_template(page_type + "/index.html")
    else:
        return abort(404)

@app.route('/fetch_data/<page_type>', methods=['GET'])
def fetch_data(page_type):
    try:
        if page_type == 'users':
            response = fetch_all_users()
        elif page_type == 'projects':
            response = fetch_all_projects()
        elif page_type == 'tasks':
            response = fetch_all_tasks()
        response_data = [entity.dump() for entity in response['entity_data']]
        response['entity_data'] = response_data
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/insert_data/<page_type>', methods=['POST'])
def insert_data(page_type):
    try:
        data = request.get_json()
        if page_type == 'users':
            response = add_new_user(data)
            return jsonify(response)
        elif page_type == 'projects':
            response = fetch_all_projects(data)
            return jsonify(response)
        elif page_type == 'tasks':
            response = fetch_all_tasks(data)
            return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
