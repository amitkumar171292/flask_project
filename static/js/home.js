"use strict";
$(function () {
    let MCubeHome = {
        init: function () {
            let that = this;
            this.base_url = window.location.origin;
            this.home_page = document.location.pathname === "/";
            that.on_load();
        },
        on_load: function () {
            console.log("On load");
            let that = this;
            // Enable item id copy
            that.copy_to_clipboard_dynamic("td.copy-item-id");
            // Page routes to load JS
            if (window.location.href.indexOf("/projects/") !== -1) {
                console.log("Projects Page");
                that.configure_projects_page();
            } else if (window.location.href.indexOf("/users/") !== -1) {
                console.log("Users Page");
                that.configure_users_page();
            } else if (window.location.href.indexOf("/tasks/") !== -1) {
                console.log("Tasks Page");
                that.configure_tasks_page();
            } else if (window.location.href.indexOf("/task-assignments/") !== -1) {
                console.log("Task Assignments Page");
                that.configure_task_assignments_page();
            }
        },
        configure_projects_page: function () {
            let that = this;
            that.fetch_entity_data('projects');
            that.add_entity_data('projects', 'add_new_project');
            that.update_entity_data('projects', "update_project");
            that.delete_entity_data('projects', "delete_project");
            that.configure_entity_datatable('projects_table', []);
        },
        configure_users_page: function () {
            let that = this;
            that.fetch_entity_data('users');
            that.add_entity_data('users', 'add_new_user');
            that.update_entity_data('users', "update_user");
            that.delete_entity_data('users', "delete_user");
            that.configure_entity_datatable('users_table', []);
        },
        configure_tasks_page: function () {
            let that = this;
            that.fetch_entity_data('tasks');
            that.add_entity_data('tasks', 'add_new_task');
            that.update_entity_data('tasks', "update_task");
            that.delete_entity_data('tasks', "delete_task");
            that.configure_entity_datatable('tasks_table', []);
        },
        configure_task_assignments_page: function () {
            let that = this;
            that.fetch_entity_data('task_assignments');
            that.add_entity_data('task-assignments', 'add_new_task_assignment');
            that.update_entity_data('task-assignments', "update_task_assignment");
            that.delete_entity_data('task-assignments', "delete_task_assignment");
            that.configure_entity_datatable('task_assignments_table', []);
        },
        configure_entity_datatable: function (data_table_id, table_data) {
            let that = this;
            let data_tables_columns = document.getElementById("data_table_column");
            let columns = that.string_to_json(data_tables_columns.dataset.columns);
            $('#'+data_table_id).DataTable({
                "destroy": true, // In order to reinitialize the datatable
                "pagination": true, // For Pagination
                "sorting": true, // For sorting
                "order": [],
                "aaData": table_data,
                "columns": columns,
            });
        },
        add_entity_data: function (entity_name, modal_id) {
            let that = this;
            let payload = {};
            let submit_form_data = document.getElementById("submit_form_data");
            let input_form = document.getElementById('add_form');
            submit_form_data.addEventListener("click", function () {
                if (!input_form.checkValidity()) {
                    input_form.classList.add('was-validated');
                } else {
                    let form_data = new FormData(input_form);
                    for (let key of form_data.keys()) {
                        payload[key] = form_data.get(key);
                    }
                    let description = document.getElementById('description');
                    if (description) {
                        payload['description'] = description.value;
                    }
                    $.ajax({
                        url: '/insert_data/'+entity_name,
                        dataType: "json",
                        type: 'POST',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify(payload),
                        success: function (data) {
                            that.default_ajax_response(modal_id, data);
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                }
            });
        },
        fetch_entity_data: function (entity_name) {
            let that = this;
            $.ajax({
                url: '/fetch_data/'+entity_name,
                type: 'GET',
                success: function (data) {
                    if (data['status']) {
                        that.configure_entity_datatable(entity_name+'_table', data['entity_data']);
                    }
                },
                error: function (error) {
                    console.error(error);
                }
            });
        },
        update_entity_data: function (entity_name, modal_id) {
            let that = this;
            let entity_data, entity_unique_id, task_id, username;
            $(document).on('click', '.update-entity', function () {
                entity_data = $(this).data('entity_data');
                entity_data = that.string_to_json(entity_data);
                if (entity_name == 'tasks') {
                    entity_unique_id = entity_data['task_id'];
                    $("#"+modal_id).find('#project_id').val(entity_data['project_id']);
                    $("#"+modal_id).find('#name').val(entity_data['name']);
                    $("#"+modal_id).find('#description').val(entity_data['description']);
                    $("#"+modal_id).find('#status').val(entity_data['status']);
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'users') {
                    entity_unique_id = entity_data['username'];
                    $("#"+modal_id).find('#name').val(entity_data['name']);
                    $("#"+modal_id).find('#phone_number').val(entity_data['phone_number']);
                    $("#"+modal_id).find('#email').val(entity_data['email']);
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'projects') {
                    entity_unique_id = entity_data['project_id'];
                    $("#"+modal_id).find('#name').val(entity_data['name']);
                    $("#"+modal_id).find('#description').val(entity_data['description']);
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'task-assignments') {
                    task_id = entity_data['task_id'];
                    username = entity_data['username'];
                    $("#"+modal_id).find('#task_id').val(task_id);
                    $("#"+modal_id).find('#username').val(username);
                }
            });
            let payload = {};
            let update_form_data = document.getElementById("update_form_data");
            let input_form = document.getElementById('update_form');
            update_form_data.addEventListener("click", function () {
                if (!input_form.checkValidity()) {
                    input_form.classList.add('was-validated');
                } else {
                    let form_data = new FormData(input_form);
                    for (let key of form_data.keys()) {
                        payload[key] = form_data.get(key);
                    }
                    let description = $('#update_form #description');
                    if (description) {
                        payload['description'] = description.val();
                    }
                    console.log(payload);
                    if (entity_name == 'task-assignments') {
                        payload['task_id'] = task_id;
                        payload['username'] = username;
                    } else {
                        payload['entity_unique_id'] = entity_unique_id;
                    }
                    $.ajax({
                        url: '/update_data/'+entity_name,
                        dataType: "json",
                        type: 'POST',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify(payload),
                        success: function (data) {
                            that.default_ajax_response(modal_id, data);
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                }
            });
        },
        delete_entity_data: function (entity_name, modal_id) {
            let that = this;
            let entity_data, entity_unique_id, task_id, username, payload={};
            $(document).on('click', '.delete-entity', function () {
                entity_data = $(this).data('entity_data');
                entity_data = that.string_to_json(entity_data);
                if (entity_name == 'tasks') {
                    entity_unique_id = entity_data['task_id'];
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'users') {
                    entity_unique_id = entity_data['username'];
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'projects') {
                    entity_unique_id = entity_data['project_id'];
                    $("#"+modal_id).find('#entity_unique_id').text(entity_unique_id);
                } else if (entity_name == 'task-assignments') {
                    task_id = entity_data['task_id'];
                    username = entity_data['username'];
                    $("#"+modal_id).find('#task_id').text(task_id);
                    $("#"+modal_id).find('#username').text(username);
                }
            });
            let delete_data = document.getElementById("delete_data");
            delete_data.addEventListener("click", function() {
                if (entity_name == 'task-assignments') {
                    payload['task_id'] = task_id;
                    payload['username'] = username;
                } else {
                    payload['entity_unique_id'] = entity_unique_id;
                }
                $.ajax({
                    url: '/delete_data/'+entity_name,
                    dataType: "json",
                    type: 'POST',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(payload),
                    success: function (data) {
                        that.default_ajax_response(modal_id, data);
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            });
        },
        default_ajax_response: function (modal_id, data) {
            let notification_message = document.getElementById("notification_message");
            notification_message.parentNode.classList.remove("d-none");
            $('#'+modal_id).modal('hide');
            if (data['status']) {
                notification_message.parentNode.classList.add("alert-success");
                notification_message.textContent = data['msg'];
            } else {
                notification_message.parentNode.classList.add("alert-danger");
                notification_message.textContent = data['msg'];
            }
            setTimeout(() => {
                notification_message.parentNode.classList.add("d-none");
                location.reload();
            }, 2000);
        },
        copy_to_clipboard_dynamic(selector, default_text = "Copy to Clipboard", copy_text = "Link Copied", inner_text = true) {
            $(document).on("click", selector, function () {
                inner_text ? navigator.clipboard.writeText(this.innerText) : navigator.clipboard.writeText(this.value);
                $(this).attr("data-original-title", copy_text);
                $(this).tooltip("update");
                $(this).tooltip("show");
            });
            $(document).on("mouseenter", selector, function () {
                $(this).attr("data-original-title", default_text);
                $(this).tooltip("update");
                $(this).tooltip("show");
            });
        },
        string_to_json(json_string) {
            try {
                json_string = json_string
                    .replace(/:[ ]*False/g, ":false")
                    .replace(/:[ ]*True/g, ":true")
                    .replace(/'/g, '"');
                return JSON.parse(json_string);
            } catch (err) {
                console.log("Could not parse, error: " + err.message);
                return null;
            }
        }
    };
    $(document).ready(function () {
        MCubeHome.init();
    });
});
