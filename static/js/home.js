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
                    "Name": "Paul",
                    "Age": 22,
                    "Location": "Canada",
                    "Contact": "+1290418345"
                },
                {
                    "Name": "Erica",
                    "Age": 32,
                    "Location": "Miami",
                    "Contact": "+1992418345"
                },
                {
                    "Name": "Pritam",
                    "Age": 29,
                    "Location": "India",
                    "Contact": "+91977418345"
                },
                {
                    "Name": "Williams",
                    "Age": 20,
                    "Location": "England",
                    "Contact": "+324290418345"
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
                    "data": "Age"
                    }, {
                    "data": "Location"
                    }, {
                    "data": "Contact"
                    }
                ]
            });
        }
    };
    $(document).ready(function () {
        MCubeHome.init();
    });
});
