-- Create a table for projects
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for users
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for tasks
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY,
    project_id INTEGER,
    description TEXT NOT NULL,
    status TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Create a table for task assignments (M:N relationship between tasks and users)
CREATE TABLE task_assignments (
    task_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (task_id, user_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
