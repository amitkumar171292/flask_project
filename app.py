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
from management.users.api import add_new_user, update_user, delete_user
from management.projects.api import add_new_project, update_project, delete_project
from management.tasks.api import add_new_task, update_task, delete_task
import requests
import json
import os

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
    data = {'project_data': []}
    if page_type == 'tasks':
         response = ProjectDB().get_all_projects()
         for project in response:
            data['project_data'].append({'action': project.project_id, 'value': project.name})
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
