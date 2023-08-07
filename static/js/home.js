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
            }
        },
        configure_projects_page: function() {
            let that = this;
            let table_data = [{
                    "Name": "Project 1",
                    "Description": "This is Project 1",
                },
                {
                    "Name": "Project 2",
                    "Description": "This is Project 2",
                },
                {
                    "Name": "Project 3",
                    "Description": "This is Project 3",
                },
                {
                    "Name": "Project 4",
                    "Description": "This is Project 4",
                }
            ];
            $('#projects_table').DataTable({
                "destroy": true, // In order to reinitialize the datatable
                "pagination": true, // For Pagination
                "sorting": true, // For sorting
                "order": [],
                "aaData": table_data,
                "columns": [{
                    "data": "Name", "searchable": true, "orderable": true
                    }, {
                    "data": "Description"
                    }
                ]
            });
        }
    };
    $(document).ready(function () {
        MCubeHome.init();
    });
});
