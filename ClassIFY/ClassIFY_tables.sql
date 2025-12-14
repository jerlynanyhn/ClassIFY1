PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS subjects (
    SubjectCode TEXT PRIMARY KEY,       -- e.g. 'CS 212'
    Name TEXT NOT NULL,
    Instructor TEXT,
    Units INTEGER,
    Goals TEXT   -- allow at least 100 characters
);

CREATE TABLE IF NOT EXISTS tasks (
    TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
    SubjectCode TEXT NOT NULL,
    TaskName TEXT NOT NULL,
    Deadline TEXT,                   -- YYYY-MM-DD
    Priority TEXT,                   -- Low / Medium / High
    Status TEXT,                     -- Not Started / In Progress / Completed
    FOREIGN KEY (SubjectCode) REFERENCES subjects(SubjectCode) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS schedule (
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    SubjectCode TEXT NOT NULL,
    Day TEXT NOT NULL,               -- 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
    StartTime TEXT NOT NULL,         -- 'HH:MM'
    EndTime TEXT NOT NULL,           -- 'HH:MM'
    Room TEXT,
    FOREIGN KEY (SubjectCode) REFERENCES subjects(SubjectCode) ON DELETE CASCADE
);
