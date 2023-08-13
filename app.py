from flask import Flask, render_template, abort, request, jsonify, get_template_attribute, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from constants import TaskStatus
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, text
from db import DbConfig
from management.users.operations import User, UserDB
from management.projects.operations import Project, ProjectDB
from management.tasks.operations import Task, TaskDB
from management.task_assignments.operations import TaskAssignment, TaskAssignmentDB
from management.users.api import add_new_user, update_user, delete_user
from management.projects.api import add_new_project, update_project, delete_project
from management.tasks.api import add_new_task, update_task, delete_task
from management.task_assignments.api import add_new_task_assignment, update_task_assignment, delete_task_assignment
import requests
import json
import os
from jinja2.exceptions import UndefinedError  # Import UndefinedError

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
    data = {}
    if page_type == 'tasks':
        data = {'project_data': [], 'user_data': []}
        response = ProjectDB().get_all_projects()
        for project in response:
            data['project_data'].append({'action': project.project_id, 'value': project.name})
    elif page_type == 'task-assignments':
        data = {'task_data': [], 'user_data': []}
        response = TaskDB().get_all_tasks()
        for task in response:
            data['task_data'].append({'action': task.task_id, 'value': task.name})
        response = UserDB().get_all_users()
        for user in response:
            data['user_data'].append({'action': user.username, 'value': f"{user.name}({user.username})"})

    page_type = page_type.replace('-', '_')

    return render_template(page_type + "/index.html", data=data)

@app.route('/fetch_data/<page_type>', methods=['GET'])
def fetch_data(page_type):
    """This route will help to fetch the data"""
    try:
        response_data = []
        response = {'status': False}
        macro_links_builder = get_template_attribute(
            "layouts/macros.html",
            "datatable_btn_builder_generic",
        )
        if page_type == 'users':
            entity_data = UserDB().get_all_users()
        elif page_type == 'projects':
            entity_data = ProjectDB().get_all_projects()
        elif page_type == 'tasks':
            entity_data = TaskDB().get_all_tasks()
        elif page_type == 'task_assignments':
            entity_data = TaskAssignmentDB().get_all_task_assignments()
        for index, entity in enumerate(entity_data):
            entity.modify = macro_links_builder(entity_name=page_type[:-1], entity_data=entity.dump())
            entity.index = index
            response_data.append(entity.dump())
        if response_data:
            response['status'] = True
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
        elif page_type == 'task-assignments':
            response = add_new_task_assignment(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400 # 400 Bad Request

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
        elif page_type == 'task-assignments':
            response = updatetask_assignment(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # 400 Bad Request

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
        elif page_type == 'task-assignments':
            response = delete_task_assignment(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # 400 Bad Request

# Route for serving favicon.ico
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

@app.route('/page-not-found')
def page_not_found():
    abort(404)

@app.route('/internal-error')
def internal_error():
    abort(500)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

@app.errorhandler(UndefinedError)
def handle_undefined_error(error):
    return render_template('error.html', error_code=500, error_message="Undefined Error"), 500  # Render custom error template

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error.html', error_code=400, error_message="Bad request"), 400

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, error_message="Forbidden"), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
