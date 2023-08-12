-- Create a table for projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for users
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    name Text NOT NULL,
    phone_number INTEGER NOT NULL,
    email TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for tasks
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Create a table for task assignments (M:N relationship between tasks and users)
CREATE TABLE task_assignments (
    task_id TEXT,
    username TEXT,
    PRIMARY KEY (task_id, username),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (username) REFERENCES users(username)
);
