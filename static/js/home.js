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
            if (window.location.href.indexOf("/projects/") !== -1) {
                console.log("Projects Page");
                that.configure_projects_page();
            } else if (window.location.href.indexOf("/users/") !== -1) {
                console.log("Users Page");
                that.configure_users_page();
            } else if (window.location.href.indexOf("/tasks/") !== -1) {
                console.log("Tasks Page");
                that.configure_tasks_page();
            }
        },
        configure_projects_page: function () {
            let that = this;
            let table_data = []
            that.fetch_entity_data('projects');
            that.configure_entity_datatable('projects_table', table_data);
            that.add_entity_data('project_form', 'projects');
        },
        configure_users_page: function () {
            let that = this;
            let table_data = []
            that.fetch_entity_data('users');
            that.configure_entity_datatable('users_table', table_data);
            that.add_entity_data('user_form', 'users');
        },
        configure_tasks_page: function () {
            let that = this;
            let table_data = []
            that.fetch_entity_data('tasks');
            that.configure_entity_datatable('tasks_table', table_data);
            that.add_entity_data('task_form', 'tasks');
        },
        configure_entity_datatable: function (data_table_id, table_data) {
            let data_tables_columns = document.getElementById("data_table_column");
            let columns = string_to_json(data_tables_columns.dataset.columns);
            function string_to_json(json_string) {
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
            $('#'+data_table_id).DataTable({
                "destroy": true, // In order to reinitialize the datatable
                "pagination": true, // For Pagination
                "sorting": true, // For sorting
                "order": [],
                "aaData": table_data,
                "columns": columns,
            });
        },
        add_entity_data: function (form_id, entity_name) {
            let payload = {};
            let submit_form_data = document.getElementById("submit_form_data");
            let input_form = document.getElementById(form_id);
            submit_form_data.addEventListener("click", function () {
                if (!input_form.checkValidity()) {
                    input_form.classList.add('was-validated');
                } else {
                    let form_data = new FormData(input_form);
                    for (let key of form_data.keys()) {
                        payload[key] = form_data.get(key);
                    }
                    $.ajax({
                        url: '/insert_data/'+entity_name,
                        dataType: "json",
                        type: 'POST',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify(payload),
                        success: function (data) {
                            let notification_message = document.getElementById("notification_message");
                            notification_message.parentNode.classList.remove("d-none");
                            $('#add_new_user').modal('hide');
                            if (data['status']) {
                                notification_message.parentNode.classList.add("alert-success");
                                notification_message.textContent = data['msg'];
                            } else {
                                notification_message.parentNode.classList.add("alert-danger");
                                notification_message.textContent = data['msg'];
                            }
                            setTimeout(() => {
                                notification_message.parentNode.classList.add("d-none");
                            }, 2000);
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
                    console.log(data);
                    if (data['status'])
                        that.configure_entity_datatable(entity_name+'_table', data['entity_data']);
                },
                error: function (error) {
                    console.error(error);
                }
            });
        }
    };
    $(document).ready(function () {
        MCubeHome.init();
    });
});
