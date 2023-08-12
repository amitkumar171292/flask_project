from flask import Flask, render_template, abort, request, jsonify, get_template_attribute
from flask_sqlalchemy import SQLAlchemy
from constants import TaskStatus
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, text
from db import DbConfig
from management.users.operations import User, UserDB
from management.projects.operations import Project, ProjectDB
from management.tasks.operations import Task, TaskDB
from management.users.api import add_new_user, update_user, delete_user, fetch_all_users
from management.projects.api import add_new_project, update_project, delete_project, fetch_all_projects
from management.tasks.api import add_new_task, update_task, delete_task, fetch_all_tasks
import requests
import json

app = Flask(__name__)

_ = DbConfig(app)

engine = create_engine('sqlite:///mcube.db')

@app.route("/")
def home():
    """This route will load the home page"""
    return render_template("home.html")

@app.route("/<page_type>/")
def pages(page_type):
    """This route will help to fetch all the data"""
    if page_type == "users":
        response = UserDB().get_all_users()
        return render_template(page_type + "/index.html")
    elif page_type == 'projects':
        response = ProjectDB().get_all_projects()
        return render_template(page_type + "/index.html")
    elif page_type == 'tasks':
        response = TaskDB().get_all_tasks()
        return render_template(page_type + "/index.html")
    else:
        return abort(404)

@app.route('/fetch_data/<page_type>', methods=['GET'])
def fetch_data(page_type):
    """This route will help to fetch the data"""
    try:
        response_data = []
        macro_links_builder = get_template_attribute(
            "layouts/macros.html",
            "datatable_btn_builder_generic",
        )
        if page_type == 'users':
            response = fetch_all_users()
        elif page_type == 'projects':
            response = fetch_all_projects()
        elif page_type == 'tasks':
            response = fetch_all_tasks()
        for index, entity in enumerate(response['entity_data']):
            if page_type == 'users':
                entity.modify = macro_links_builder(entity_name=page_type[:-1], entity_unique_id=entity.username)
            elif page_type == 'projects':
                entity.modify = macro_links_builder(entity_name=page_type[:-1], entity_unique_id=entity.project_id)
            elif page_type == 'tasks':
                entity.modify = macro_links_builder(entity_name=page_type[:-1], entity_unique_id=entity.task_id)
            entity.index = index
            response_data.append(entity.dump())
        response['entity_data'] = response_data
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/insert_data/<page_type>', methods=['POST'])
def insert_data(page_type):
    """This route will help to insert the data"""
    try:
        data = request.get_json()
        if page_type == 'users':
            response = add_new_user(data)
        elif page_type == 'projects':
            response = add_new_project(data)
        elif page_type == 'tasks':
            response = add_new_task(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/update_data/<page_type>', methods=['POST'])
def update_data(page_type):
    """This route will help to update the data"""
    try:
        data = request.get_json()
        if page_type == 'users':
            response = update_user(data)
        elif page_type == 'projects':
            response = update_project(data)
        elif page_type == 'tasks':
            response = update_task(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/delete_data/<page_type>', methods=['POST'])
def delete_data(page_type):
    """This route will help to update the data"""
    try:
        data = request.get_json()
        if page_type == 'users':
            response = delete_user(data)
        elif page_type == 'projects':
            response = delete_project(data)
        elif page_type == 'tasks':
            response = delete_task(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
