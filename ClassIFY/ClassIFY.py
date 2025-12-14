import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, date, timedelta
import calendar as cal
import csv
import os

class Database: # Responsible for handling all database operations
    
    def __init__(self, db_path='ClassIFY.db'): # ClassIFY.db is created and connected automatically when the program runs
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
        
    def init_database(self):
        self.conn = sqlite3.connect(self.db_path) # Establish the actual connection between the GUI and the database
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.seed_data_if_empty()
        self.write_schema_files()
        print(f"✅ Database initialized: {self.db_path}")
        
    def create_tables(self):
        tables = [
            """CREATE TABLE IF NOT EXISTS subjects (
                SubjectCode TEXT PRIMARY KEY,       -- e.g. 'CS 212'
                Name TEXT NOT NULL,
                Instructor TEXT,
                Units INTEGER,
                Goals TEXT                         -- allows up to 100 characters
            )""",
            """CREATE TABLE IF NOT EXISTS tasks (
                TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
                SubjectCode TEXT NOT NULL,
                TaskName TEXT NOT NULL,
                Deadline TEXT,                     -- YYYY-MM-DD
                Priority TEXT,                     -- Low / Medium / High
                Status TEXT,                       -- Not Started / In Progress / Completed
                FOREIGN KEY (SubjectCode) REFERENCES subjects(SubjectCode) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS schedule (
                ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
                SubjectCode TEXT NOT NULL,
                Day TEXT NOT NULL,                 -- 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
                StartTime TEXT NOT NULL,           -- 'HH:MM'
                EndTime TEXT NOT NULL,             -- 'HH:MM'
                Room TEXT,
                FOREIGN KEY (SubjectCode) REFERENCES subjects(SubjectCode) ON DELETE CASCADE
            )"""
        ]
        
        for table_sql in tables:
            self.cursor.execute(table_sql)
        self.conn.commit()
        
    def seed_data_if_empty(self):
        self.cursor.execute("SELECT COUNT(*) FROM subjects")
        subjects_count = self.cursor.fetchone()[0]
        
        if subjects_count == 0:
            print("📝 Seeding database with sample data...")
            
            subjects = [
                ('CS 212', 'Computer Organization with Assembly Language', 'DELA CRUZ, MAURICE OLIVER Y.', 3, 'Learn how assembler and compiler works'),
                ('GEd 109', 'Science, Technology and Society', 'MAGADIA, GLEN FERDINAND C.', 3, 'Defend the research project!'),
                ('CS 211', 'Object-Oriented Programming', 'AGDON, FATIMA MARIE P.', 3, 'Learn more about OOP Java and able to apply on some projects'),
                ('PATHFit 3', 'Traditional and Recreational Games', 'DE CASTRO, JOEY R.', 3, 'Learn how to play table tennis and have a healthy lifestyle'),
                ('Phy 101', 'Calculus-Based Physics', 'MENDOZA, BABY KAREN L.', 3, 'Understand all the lessons'),
                ('CpE 405', 'Discrete Mathematics', 'BAGSIT, CHARLES CONRAD P.', 3, 'Learn more about logics with math!'),
                ('IT 212', 'Computer Networking 1', 'MACATANGAY, LLOYD H.', 3, 'Get CISCO NetAcad certification')
            ]
            
            self.cursor.executemany(
                "INSERT INTO subjects (SubjectCode, Name, Instructor, Units, Goals) VALUES (?, ?, ?, ?, ?)",
                subjects
            )
            
            tasks = [
                ('CpE 405', 'Review for final exam', '2025-12-12', 'High', 'Not Started'),
                ('CS 211', 'Review for final exam', '2025-12-09', 'High', 'Not Started'),
                ('CS 211', 'Review for quiz', '2025-12-09', 'High', 'In Progress'),
                ('CS 212', 'Review for final exam and practice coding with assembly language', '2025-12-11', 'High', 'Not Started'),
                ('Phy 101', 'Successfully defend the research project in Physics and STS', '2025-12-04', 'High', 'Completed')
            ]
            
            self.cursor.executemany(
                "INSERT INTO tasks (SubjectCode, TaskName, Deadline, Priority, Status) VALUES (?, ?, ?, ?, ?)",
                tasks
            )
            
            schedule = [
                ('Phy 101', 'Mon', '10:00', '13:00', 'ROOM 402'),
                ('GEd 109', 'Mon', '14:00', '17:00', 'ROOM 101'),
                ('CS 211', 'Tue', '07:00', '10:00', 'LAB 02'),
                ('Phy 101', 'Tue', '11:00', '13:00', 'ROOM 105'),
                ('IT 212', 'Wed', '10:00', '13:00', 'LAB 06'),
                ('PATHFit 3', 'Wed', '14:00', '16:00', 'GYM'),
                ('CS 211', 'Thu', '07:00', '09:00', 'ONLINE'),
                ('IT 212', 'Thu', '14:00', '16:00', 'ONLINE'),
                ('CS 212', 'Thu', '11:00', '13:00', 'ONLINE'),
                ('CS 212', 'Fri', '07:00', '10:00', 'LAB 03'),
                ('CpE 405', 'Sat', '07:00', '10:00', 'ROOM 103')
            ]
            
            self.cursor.executemany(
                "INSERT INTO schedule (SubjectCode, Day, StartTime, EndTime, Room) VALUES (?, ?, ?, ?, ?)",
                schedule
            )
            
            self.conn.commit()
            print("✅ Sample data inserted successfully!")
        else:
            print("✅ Database already contains data")
            
    def write_schema_files(self):
        try:
            #Write ClassIFY_tables.sql
            tables_sql = """PRAGMA foreign_keys = ON;

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
"""
            
            with open('ClassIFY_tables.sql', 'w', encoding='utf-8') as f:
                f.write(tables_sql)
            
            # Write ClassIFY_data.sql with the exact seed data - FIXED
            data_sql = """-- Subjects
INSERT INTO subjects (SubjectCode, Name, Instructor, Units, Goals) VALUES
('CS 212', 'Computer Organization with Assembly Language', 'DELA CRUZ, MAURICE OLIVER Y.', 3, 'Learn how assembler and compiler works'),
('GEd 109', 'Science, Technology and Society', 'MAGADIA, GLEN FERDINAND C.', 3, 'Defend the research project!'),
('CS 211', 'Object-Oriented Programming', 'AGDON, FATIMA MARIE P.', 3, 'Learn more about OOP Java and able to apply on some projects'),
('PATHFit 3', 'Traditional and Recreational Games', 'DE CASTRO, JOEY R.', 3, 'Learn how to play table tennis and have a healthy lifestyle'),
('Phy 101', 'Calculus-Based Physics', 'MENDOZA, BABY KAREN L.', 3, 'Understand all the lessons'),
('CpE 405', 'Discrete Mathematics', 'BAGSIT, CHARLES CONRAD P.', 3, 'Learn more about logics with math!'),
('IT 212', 'Computer Networking 1', 'MACATANGAY, LLOYD H.', 3, 'Get CISCO NetAcad certification');

-- Tasks
INSERT INTO tasks (SubjectCode, TaskName, Deadline, Priority, Status) VALUES
('CpE 405', 'Review for final exam', '2025-12-12', 'High', 'Not Started'),
('CS 211', 'Review for final exam', '2025-12-09', 'High', 'Not Started'),
('CS 211', 'Review for quiz', '2025-12-09', 'High', 'In Progress'),
('CS 212', 'Review for final exam \n and practice coding with assembly language', '2025-12-11', 'High', 'Not Started'),
('Phy 101', 'Successfully defend the research project in Physics and STS', '2025-12-04', 'High', 'Completed');

-- Schedule
INSERT INTO schedule (SubjectCode, Day, StartTime, EndTime, Room) VALUES
('Phy 101', 'Mon', '10:00', '13:00', 'ROOM 402'),
('GEd 109', 'Mon', '14:00', '17:00', 'ROOM 101'),
('CS 211', 'Tue', '07:00', '10:00', 'LAB 02'),
('Phy 101', 'Tue', '11:00', '13:00', 'ROOM 105'),
('IT 212', 'Wed', '10:00', '13:00', 'LAB 06'),
('PATHFit 3', 'Wed', '14:00', '16:00', 'GYM'),
('CS 211', 'Thu', '07:00', '09:00', 'ONLINE'),
('IT 212', 'Thu', '14:00', '16:00', 'ONLINE'),
('CS 212', 'Thu', '11:00', '13:00', 'ONLINE'),
('CS 212', 'Fri', '07:00', '10:00', 'LAB 03'),
('CpE 405', 'Sat', '07:00', '10:00', 'ROOM 103');
"""
            
            with open('ClassIFY_data.sql', 'w', encoding='utf-8') as f:
                f.write(data_sql)
                
            print("✅ Generated ClassIFY_tables.sql and ClassIFY_data.sql")
            
        except Exception as e:
            print(f"⚠️ Could not write SQL files: {e}")
    
    def get_subjects(self):
        """Get all subjects"""
        self.cursor.execute("SELECT * FROM subjects ORDER BY SubjectCode")
        return self.cursor.fetchall()
    
    def get_subject_by_code(self, subject_code):
        """Get subject by SubjectCode"""
        self.cursor.execute("SELECT * FROM subjects WHERE SubjectCode = ?", (subject_code,))
        return self.cursor.fetchone()
    
    def add_subject(self, code, name, instructor, units, goals):
        """Add a new subject using SubjectCode as primary key"""
        self.cursor.execute(
            "INSERT INTO subjects (SubjectCode, Name, Instructor, Units, Goals) VALUES (?, ?, ?, ?, ?)",
            (code, name, instructor, units, goals)
        )
        self.conn.commit()
        return code
    
    def update_subject(self, old_code, new_code, name, instructor, units, goals):
        """Update a subject - handles SubjectCode change"""
        try:
            # If SubjectCode changed, update foreign keys first
            if old_code != new_code:
                # Update tasks
                self.cursor.execute("UPDATE tasks SET SubjectCode = ? WHERE SubjectCode = ?", 
                                  (new_code, old_code))
                
                # Update schedule
                self.cursor.execute("UPDATE schedule SET SubjectCode = ? WHERE SubjectCode = ?", 
                                  (new_code, old_code))
            
            self.cursor.execute(
                """UPDATE subjects SET SubjectCode=?, Name=?, Instructor=?, Units=?, Goals=?
                   WHERE SubjectCode=?""",
                (new_code, name, instructor, units, goals, old_code)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def delete_subject(self, subject_code):
        """Delete a subject (cascades to tasks and schedule via FK)"""
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete subject '{subject_code}'?\n\nThis will delete ALL associated tasks and schedule entries!"):
            self.cursor.execute("DELETE FROM subjects WHERE SubjectCode = ?", (subject_code,))
            self.conn.commit()
            return True
        return False
    
    def get_tasks(self, subject_code=None):
        """Get tasks, optionally filtered by SubjectCode"""
        if subject_code:
            query = """SELECT t.*, s.Name FROM tasks t 
                      JOIN subjects s ON t.SubjectCode = s.SubjectCode 
                      WHERE t.SubjectCode = ? 
                      ORDER BY t.Deadline"""
            self.cursor.execute(query, (subject_code,))
        else:
            query = """SELECT t.*, s.Name FROM tasks t 
                      JOIN subjects s ON t.SubjectCode = s.SubjectCode 
                      ORDER BY t.Deadline"""
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_todays_tasks(self):
        """Get tasks due today"""
        today = str(date.today())
        query = """SELECT t.*, s.SubjectCode, s.Name FROM tasks t 
                  JOIN subjects s ON t.SubjectCode = s.SubjectCode 
                  WHERE t.Deadline = ? 
                  ORDER BY CASE t.Priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END"""
        self.cursor.execute(query, (today,))
        return self.cursor.fetchall()
    
    def add_task(self, subject_code, task_name, deadline, priority, status):
        """Add a new task using SubjectCode as FK"""
        self.cursor.execute(
            """INSERT INTO tasks (SubjectCode, TaskName, Deadline, Priority, Status)
               VALUES (?, ?, ?, ?, ?)""",
            (subject_code, task_name, deadline, priority, status)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_task(self, task_id, subject_code, task_name, deadline, priority, status):
        """Update a task using TaskID"""
        self.cursor.execute(
            """UPDATE tasks SET SubjectCode=?, TaskName=?, Deadline=?, Priority=?, Status=?
               WHERE TaskID=?""",
            (subject_code, task_name, deadline, priority, status, task_id)
        )
        self.conn.commit()
    
    def delete_task(self, task_id):
        """Delete a task by TaskID"""
        self.cursor.execute("DELETE FROM tasks WHERE TaskID = ?", (task_id,))
        self.conn.commit()
    
    def get_schedule(self, day=None):
        """Get schedule entries, optionally filtered by day using SubjectCode as FK"""
        if day:
            query = """SELECT s.*, subj.Name FROM schedule s
                      JOIN subjects subj ON s.SubjectCode = subj.SubjectCode
                      WHERE s.Day = ? ORDER BY s.StartTime"""
            self.cursor.execute(query, (day,))
        else:
            query = """SELECT s.*, subj.Name FROM schedule s
                      JOIN subjects subj ON s.SubjectCode = subj.SubjectCode
                      ORDER BY 
                      CASE s.Day 
                          WHEN 'Mon' THEN 1
                          WHEN 'Tue' THEN 2
                          WHEN 'Wed' THEN 3
                          WHEN 'Thu' THEN 4
                          WHEN 'Fri' THEN 5
                          WHEN 'Sat' THEN 6
                          WHEN 'Sun' THEN 7
                          ELSE 8
                      END,
                      s.StartTime"""
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_todays_schedule(self):
        """Get today's schedule based on current weekday"""
        today = date.today()
        weekday_num = today.weekday()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        today_day = days[weekday_num]
        return self.get_schedule(today_day)
    
    def add_schedule(self, subject_code, day, start_time, end_time, room):
        """Add a new schedule entry using SubjectCode as FK"""
        self.cursor.execute(
            """INSERT INTO schedule (SubjectCode, Day, StartTime, EndTime, Room)
               VALUES (?, ?, ?, ?, ?)""",
            (subject_code, day, start_time, end_time, room)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_schedule(self, schedule_id, subject_code, day, start_time, end_time, room):
        """Update a schedule entry using ScheduleID"""
        self.cursor.execute(
            """UPDATE schedule SET SubjectCode=?, Day=?, StartTime=?, EndTime=?, Room=?
               WHERE ScheduleID=?""",
            (subject_code, day, start_time, end_time, room, schedule_id)
        )
        self.conn.commit()
    
    def delete_schedule(self, schedule_id):
        """Delete a schedule entry by ScheduleID"""
        self.cursor.execute("DELETE FROM schedule WHERE ScheduleID = ?", (schedule_id,))
        self.conn.commit()
    
    # REPORT QUERIES - Updated to match requested filters
    def get_all_subjects_with_tasks(self):
        """Report: All subjects with their tasks"""
        query = """SELECT s.SubjectCode, s.Name, s.Instructor, s.Units,
                  GROUP_CONCAT(t.TaskName || ' (Due: ' || t.Deadline || ', ' || t.Status || ')', '; ') as Tasks
                  FROM subjects s
                  LEFT JOIN tasks t ON s.SubjectCode = t.SubjectCode
                  GROUP BY s.SubjectCode, s.Name, s.Instructor, s.Units
                  ORDER BY s.SubjectCode"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_upcoming_tasks(self):
        """Report: Upcoming tasks (from tomorrow forward)"""
        query = """SELECT t.TaskName, t.Deadline, t.Priority, t.Status, s.SubjectCode, s.Name
                  FROM tasks t
                  JOIN subjects s ON t.SubjectCode = s.SubjectCode
                  WHERE date(t.Deadline) > date('now')
                  ORDER BY date(t.Deadline) ASC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_tasks_today(self):
        """Report: Tasks due today"""
        query = """SELECT t.TaskName, t.Deadline, t.Priority, t.Status, s.SubjectCode, s.Name
                  FROM tasks t
                  JOIN subjects s ON t.SubjectCode = s.SubjectCode
                  WHERE date(t.Deadline) = date('now')
                  ORDER BY t.Priority DESC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_completed_tasks(self):
        """Report: Completed tasks"""
        query = """SELECT t.TaskName, t.Deadline, t.Priority, t.Status, s.SubjectCode, s.Name
                  FROM tasks t
                  JOIN subjects s ON t.SubjectCode = s.SubjectCode
                  WHERE t.Status = 'Completed'
                  ORDER BY t.Deadline DESC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_missing_tasks(self):
        """Report: Missing/overdue tasks (past deadline and not completed)"""
        query = """SELECT t.TaskName, t.Deadline, t.Priority, t.Status, s.SubjectCode, s.Name
                  FROM tasks t
                  JOIN subjects s ON t.SubjectCode = s.SubjectCode
                  WHERE date(t.Deadline) < date('now') AND t.Status != 'Completed'
                  ORDER BY t.Deadline ASC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_schedule_for_today(self):
        """Report: Schedule for today"""
        today = date.today()
        weekday_num = today.weekday()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        today_day = days[weekday_num]
        
        query = """SELECT s.SubjectCode, sub.Name, s.StartTime, s.EndTime, s.Room
                  FROM schedule s
                  JOIN subjects sub ON s.SubjectCode = sub.SubjectCode
                  WHERE s.Day = ?
                  ORDER BY s.StartTime"""
        self.cursor.execute(query, (today_day,))
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class ClassifyApp:
    """Main application class with SubjectCode as primary key for all tables"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Class-i-fy: A student organizer built just for YOU")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Start maximized
        
        # Set font sizes for better readability
        self.fonts = {
            'header': ('Arial', 28, 'bold'),
            'subheader': ('Arial', 20, 'bold'),
            'normal': ('Arial', 16),
            'small': ('Arial', 14),
            'button': ('Arial', 14, 'bold'),
            'table': ('Arial', 13)
        }
        
        # Color palette - FIXED: Restored original priority colors
        self.colors = {
            'deep_maroon': '#610027',
            'deep_crimson': '#912B48',
            'dusty_pink': '#B45A69',
            'soft_pink': '#FCD0D9',
            'card_bg': '#FFFFFF',
            'text_primary': '#2C2C2C',
            'text_secondary': '#5A5A5A',
            'accent_light': '#FFE8EC',
            'hover': '#B45A69',
            'success': '#4CAF50', #GREEN
            'warning': '#FF9800',
            'high_priority': '#8B0000', #DARK RED
            'medium_priority': '#008080', #TEAL
            'low_priority': '#2C2C2C'        #BLACK
        }
        
        # Motivational quotes
        self.quotes = [
            "💫 The future depends on what you do today. - Mahatma Gandhi",
            "💫 Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
            "💫 The only way to do great work is to love what you do. - Steve Jobs",
            "💫 Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "💫 The expert in anything was once once a beginner. - Helen Hayes"
        ]
        
        # Initialize database
        self.db = Database()
        
        # Setup styles
        self.setup_styles()
        
        # Create main container
        self.main_container = tk.Frame(root, bg=self.colors['soft_pink'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create navigation
        self.create_navigation()
        
        # Create content area
        self.create_content_area()
        
        # Show dashboard initially
        self.show_dashboard()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_styles(self):
        """Configure premium styles with larger fonts"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Navigation button styles
        style.configure('Nav.TButton',
                       background=self.colors['deep_crimson'],
                       foreground='white',
                       borderwidth=0,
                       padding=(30, 20),
                       font=self.fonts['button'],
                       relief='flat')
        
        style.configure('NavActive.TButton',
                       background=self.colors['deep_maroon'],
                       foreground='white',
                       borderwidth=0,
                       padding=(30, 20),
                       font=self.fonts['button'],
                       relief='flat')
        
        # Primary button style
        style.configure('Primary.TButton',
                       background=self.colors['deep_maroon'],
                       foreground='white',
                       borderwidth=0,
                       padding=(25, 15),
                       font=self.fonts['button'])
        
        # Secondary button style
        style.configure('Secondary.TButton',
                       background=self.colors['dusty_pink'],
                       foreground='white',
                       borderwidth=0,
                       padding=(20, 12),
                       font=self.fonts['small'])
        
        # Treeview style
        style.configure('Pastel.Treeview',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['card_bg'],
                       borderwidth=0,
                       rowheight=40,
                       font=self.fonts['table'])
        
        style.configure('Pastel.Treeview.Heading',
                       background=self.colors['dusty_pink'],
                       foreground='white',
                       borderwidth=0,
                       font=self.fonts['table'],
                       padding=10)
        
        style.map('Pastel.Treeview.Heading',
                 background=[('active', self.colors['deep_crimson'])])
    
    def create_header(self):
        """Create the premium header with readable fonts"""
        header_frame = tk.Frame(self.main_container, 
                               bg=self.colors['deep_maroon'], 
                               height=160,
                               relief='flat')
        header_frame.pack(fill='x', pady=(0, 25))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="✎ ClassIFY: A Student Academic Organizer Built Just For I and FOR YOUᝰ",
                              font=self.fonts['header'],
                              bg=self.colors['deep_maroon'],
                              fg='white',
                              pady=35)
        title_label.pack(expand=True)
    
    def create_navigation(self):
        """Create premium navigation"""
        nav_frame = tk.Frame(self.main_container, bg=self.colors['soft_pink'])
        nav_frame.pack(fill='x', pady=(0, 25))
        
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", self.show_dashboard),
            ("📚 Subjects", self.show_subjects),
            ("✔ Tasks", self.show_tasks),
            ("🕒 Schedule", self.show_schedule),
            ("📁 Records", self.show_records)
        ]
        
        for text, command in nav_items:
            btn = ttk.Button(nav_frame, text=text, command=command, style='Nav.TButton')
            btn.pack(side='left', padx=5)
            self.nav_buttons[text] = btn
        
        self.set_active_nav("🏠 Home")
    
    def set_active_nav(self, active_button):
        """Set active navigation button"""
        for text, btn in self.nav_buttons.items():
            if text == active_button:
                btn.configure(style='NavActive.TButton')
            else:
                btn.configure(style='Nav.TButton')
    
    def create_content_area(self):
        """Create content area"""
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['soft_pink'])
        self.content_frame.pack(fill='both', expand=True)
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        self.set_active_nav("🏠 Home")
        
        #Motivational quote
        import random
        quote_frame = tk.Frame(self.content_frame, bg=self.colors['dusty_pink'], height=80)
        quote_frame.pack(fill='x', pady=(0, 30))
        quote_frame.pack_propagate(False)
        
        quote_label = tk.Label(quote_frame,
                              text=random.choice(self.quotes),
                              font=self.fonts['normal'],
                              bg=self.colors['dusty_pink'],
                              fg='white',
                              wraplength=1300)
        quote_label.pack(expand=True, padx=20)
        
        #Main content
        main_content = tk.Frame(self.content_frame, bg=self.colors['soft_pink'])
        main_content.pack(fill='both', expand=True)
        
        left_column = tk.Frame(main_content, bg=self.colors['soft_pink'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        right_column = tk.Frame(main_content, bg=self.colors['soft_pink'])
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        #Today's Classes - Full width
        self.create_card(left_column, "📚 Today's Classes", self.colors['deep_crimson'], 
                        self.get_todays_classes_content, pady=(0, 20), width=600)
        
        #Today's To-Dos - Full width
        self.create_card(left_column, "📝 Today's To-Do List", self.colors['dusty_pink'], 
                        self.get_todays_todos_content, pady=(20, 0), width=600)
        
        #Calendar - Full width
        self.create_card(right_column, "📅 Monthly Calendar", self.colors['deep_maroon'], 
                        self.get_calendar_content, pady=(0, 20), width=600)
        
        #Quick Goals Overview - Full width
        self.create_card(right_column, "🎯 Subjects with Goals", self.colors['deep_crimson'], 
                        self.get_subjects_goals_content, pady=(0, 20), width=600)
    
    def create_card(self, parent, title, title_color, content_callback, width=500, **kwargs):
        card_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat')
        card_frame.pack(fill='both', expand=True, **kwargs)
        
        #Card header
        header_frame = tk.Frame(card_frame, bg=title_color, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text=title,
                              font=self.fonts['subheader'],
                              bg=title_color,
                              fg='white')
        title_label.pack(expand=True)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['card_bg'], padx=25, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        content_callback(content_frame)
    
    def get_subjects_goals_content(self, parent):
        """Content for Subjects with Goals card - full width - EXACT FROM SECOND CODE"""
        subjects = self.db.get_subjects()
        
        if not subjects:
            no_subjects = tk.Label(parent,
                                  text="No subjects added yet!",
                                  font=self.fonts['normal'],
                                  bg=self.colors['card_bg'],
                                  fg=self.colors['text_secondary'],
                                  justify='center')
            no_subjects.pack(expand=True, pady=20)
            return
        
        # Create a frame with scrollbar - full width
        container = tk.Frame(parent, bg=self.colors['card_bg'])
        container.pack(fill='both', expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(container, bg=self.colors['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card_bg'], width=550)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=550)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, subject in enumerate(subjects):
            bg_color = self.colors['accent_light'] if i % 2 == 0 else self.colors['card_bg']
            subject_frame = tk.Frame(scrollable_frame, bg=bg_color)
            subject_frame.pack(fill='x', pady=8, padx=10)
            
            # Full width display
            subject_text = f"📖 {subject[0]} - {subject[1]}"
            if subject[4]:  # Goals
                goal_text = subject[4]
                subject_text += f"\n   🎯 {goal_text}"
            
            subject_label = tk.Label(subject_frame,
                                    text=subject_text,
                                    font=self.fonts['normal'],
                                    bg=bg_color,
                                    fg=self.colors['text_primary'],
                                    justify='left',
                                    anchor='w',
                                    wraplength=500)
            subject_label.pack(fill='x', padx=20, pady=12)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def get_todays_classes_content(self, parent):
        """Content for Today's Classes card showing SubjectCode - full width - EXACT FROM SECOND CODE"""
        schedule = self.db.get_todays_schedule()
        
        if not schedule:
            no_classes = tk.Label(parent,
                                text="No classes scheduled for today! 🎉",
                                font=self.fonts['normal'],
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_secondary'],
                                justify='center')
            no_classes.pack(expand=True, pady=30)
            return
        
        for i, entry in enumerate(schedule):
            bg_color = self.colors['accent_light'] if i % 2 == 0 else self.colors['card_bg']
            class_frame = tk.Frame(parent, bg=bg_color)
            class_frame.pack(fill='x', pady=10)
            
            class_text = f"🕒 {entry[3]} - {entry[4]}\n📖 {entry[1]} ({entry[6]})\n📍 {entry[5] or 'No room'}"
            class_label = tk.Label(class_frame,
                                  text=class_text,
                                  font=self.fonts['normal'],
                                  bg=bg_color,
                                  fg=self.colors['text_primary'],
                                  justify='left',
                                  anchor='w')
            class_label.pack(fill='x', padx=20, pady=12)
    
    def get_todays_todos_content(self, parent):
        """Content for Today's To-Dos card showing SubjectCode - full width - EXACT FROM SECOND CODE"""
        tasks = self.db.get_todays_tasks()
        
        if not tasks:
            no_tasks = tk.Label(parent,
                               text="No tasks due today! ✅",
                               font=self.fonts['normal'],
                               bg=self.colors['card_bg'],
                               fg=self.colors['text_secondary'],
                               justify='center')
            no_tasks.pack(expand=True, pady=30)
            return
        
        for i, task in enumerate(tasks):
            bg_color = self.colors['accent_light'] if i % 2 == 0 else self.colors['card_bg']
            task_frame = tk.Frame(parent, bg=bg_color)
            task_frame.pack(fill='x', pady=8)
            
            # Color code by priority
            priority_color = {
                'High': self.colors['high_priority'],      # '#FF4444' (RED)
                'Medium': self.colors['medium_priority'],  # '#FFAA66' (ORANGE)
                'Low': self.colors['low_priority']         # '#66CC66' (GREEN)
            }.get(task[4], self.colors['text_primary'])
            
            # Check if overdue
            if datetime.strptime(task[3], '%Y-%m-%d').date() < date.today():
                priority_color = self.colors['high_priority']  # '#FF4444' (RED)
            
            status_icon = '✅' if task[5] == 'Completed' else '⏳' if task[5] == 'In Progress' else '📝'
            task_text = f"{status_icon} {task[2]}\n   📚 {task[6]} ({task[1]})"
            task_label = tk.Label(task_frame,
                                 text=task_text,
                                 font=self.fonts['normal'],
                                 bg=bg_color,
                                 fg=priority_color,
                                 justify='left',
                                 anchor='w')
            task_label.pack(fill='x', padx=20, pady=10)
    
    def get_calendar_content(self, parent):
        """Content for Calendar card - shows tasks with SubjectCode - EXACT FROM SECOND CODE"""
        # Try to use tkcalendar if available
        try:
            from tkcalendar import Calendar
            calendar_frame = tk.Frame(parent, bg=self.colors['card_bg'])
            calendar_frame.pack(fill='both', expand=True)
            
            cal = Calendar(calendar_frame,
                          selectmode='day',
                          date_pattern='yyyy-mm-dd',
                          background=self.colors['card_bg'],
                          foreground=self.colors['text_primary'],
                          font=self.fonts['normal'],
                          showweeknumbers=False,
                          borderwidth=2,
                          relief='solid',
                          width=550,
                          height=300)
            cal.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Bind click event
            cal.bind('<<CalendarSelected>>', self.on_calendar_date_selected)
            self.calendar = cal
            
        except ImportError:
            # Fallback calendar
            fallback_label = tk.Label(parent,
                                     text="Install tkcalendar for enhanced calendar:\npip install tkcalendar",
                                     font=self.fonts['small'],
                                     bg=self.colors['card_bg'],
                                     fg=self.colors['deep_crimson'],
                                     pady=20)
            fallback_label.pack()
            
            # Simple month view
            today = date.today()
            month_frame = tk.Frame(parent, bg=self.colors['card_bg'])
            month_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            month_label = tk.Label(month_frame,
                                  text=today.strftime("%B %Y"),
                                  font=self.fonts['subheader'],
                                  bg=self.colors['card_bg'],
                                  fg=self.colors['deep_maroon'])
            month_label.pack(pady=10)
    
    def on_calendar_date_selected(self, event):
        """Handle calendar date selection - shows tasks with SubjectCode"""
        selected_date = self.calendar.get_date()
        
        # Get tasks for selected date using SubjectCode
        tasks = self.db.get_tasks()
        date_tasks = [t for t in tasks if t[3] == selected_date]
        
        if date_tasks:
            task_list = "\n".join([f"• {task[2]} ({task[1]}) - Priority: {task[4]}" for task in date_tasks])
            messagebox.showinfo(f"Tasks for {selected_date}", task_list)
        else:
            messagebox.showinfo(f"Tasks for {selected_date}", "No tasks due on this date")
    
    def show_toast(self, message):
        """Show a success toast message"""
        toast = tk.Label(self.root, text=message, bg=self.colors['success'], 
                        fg='white', font=self.fonts['small'], padx=25, pady=15)
        toast.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        self.root.after(2000, toast.destroy)
    
    def show_subjects(self):
        """Show subjects management page with Goals character limit"""
        self.clear_content()
        self.set_active_nav("📚 Subjects")
        
        # Header
        header = tk.Label(self.content_frame,
                         text="📚 Subjects Management",
                         font=self.fonts['header'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'])
        header.pack(pady=(0, 25))
        
        # Control frame
        control_frame = tk.Frame(self.content_frame, bg=self.colors['soft_pink'])
        control_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Button(control_frame, text="+ Add New Subject",
                  command=self.add_subject_dialog, style='Primary.TButton').pack(side='left', padx=5)
        
        # Subjects table
        self.create_subjects_table()
    
    def create_subjects_table(self):
        """Create subjects table showing SubjectCode - FULL WIDTH"""
        table_container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        table_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview - FULL WIDTH
        columns = ('SubjectCode', 'Name', 'Instructor', 'Units', 'Goals')
        self.subjects_tree = ttk.Treeview(table_container, columns=columns, show='headings', 
                                         height=15, style='Pastel.Treeview')
        
        # Configure columns - WIDER COLUMNS
        self.subjects_tree.heading('SubjectCode', text='Subject Code')
        self.subjects_tree.heading('Name', text='Name')
        self.subjects_tree.heading('Instructor', text='Instructor')
        self.subjects_tree.heading('Units', text='Units')
        self.subjects_tree.heading('Goals', text='Goals')
        
        # Set column widths - FULL WIDTH
        self.subjects_tree.column('SubjectCode', width=150, stretch=True)
        self.subjects_tree.column('Name', width=300, stretch=True)
        self.subjects_tree.column('Instructor', width=250, stretch=True)
        self.subjects_tree.column('Units', width=100, stretch=True)
        self.subjects_tree.column('Goals', width=400, stretch=True)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_container, orient='vertical', command=self.subjects_tree.yview)
        hsb = ttk.Scrollbar(table_container, orient='horizontal', command=self.subjects_tree.xview)
        self.subjects_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.subjects_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew', columnspan=2)
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Load data
        self.load_subjects_data()
        
        # Action buttons
        action_frame = tk.Frame(self.content_frame, bg=self.colors['soft_pink'], pady=15)
        action_frame.pack(fill='x')
        
        ttk.Button(action_frame, text="✏️ Edit Selected", 
                  command=self.edit_subject_dialog, style='Secondary.TButton').pack(side='left', padx=8)
        ttk.Button(action_frame, text="🗑️ Delete Selected", 
                  command=self.delete_subject, style='Secondary.TButton').pack(side='left', padx=8)
        ttk.Button(action_frame, text="🔄 Refresh", 
                  command=self.load_subjects_data, style='Secondary.TButton').pack(side='left', padx=8)
    
    def load_subjects_data(self):
        """Load subjects data using SubjectCode"""
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
        
        subjects = self.db.get_subjects()
        for i, subject in enumerate(subjects):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.subjects_tree.insert('', 'end', values=subject, tags=(tag,))
        
        self.subjects_tree.tag_configure('even', background=self.colors['card_bg'])
        self.subjects_tree.tag_configure('odd', background=self.colors['accent_light'])
    
    def add_subject_dialog(self):
        """Dialog for adding a subject with Goals character limit"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Subject")
        dialog.geometry("650x550")
        dialog.configure(bg=self.colors['soft_pink'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        header = tk.Label(dialog,
                         text="Add New Subject",
                         font=self.fonts['subheader'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'],
                         pady=20)
        header.pack(fill='x')
        
        form_frame = tk.Frame(dialog, bg=self.colors['card_bg'], padx=40, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        fields = [
            ("Subject Code:", "code"),
            ("Subject Name:", "name"),
            ("Instructor:", "instructor"),
            ("Units:", "units"),
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label, 
                    bg=self.colors['card_bg'],
                    font=self.fonts['small']).grid(row=i, column=0, sticky='e', pady=15, padx=(0, 20))
            
            entry = tk.Entry(form_frame, width=35, font=self.fonts['small'],
                            bg=self.colors['accent_light'])
            entry.grid(row=i, column=1, pady=15, sticky='w')
            entries[field] = entry
        
        # Goals with character counter
        tk.Label(form_frame, text="Goals (max 100 chars):", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=4, column=0, sticky='ne', pady=15, padx=(0, 20))
        
        goals_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        goals_frame.grid(row=4, column=1, pady=15, sticky='w')
        
        goals_text = tk.Text(goals_frame, height=5, width=35, font=self.fonts['small'],
                            bg=self.colors['accent_light'])
        goals_text.pack(side='left')
        entries['goals'] = goals_text
        
        # Character counter
        char_counter = tk.Label(goals_frame, text="100", 
                               bg=self.colors['card_bg'], font=self.fonts['small'],
                               fg=self.colors['text_secondary'])
        char_counter.pack(side='left', padx=10)
        
        def update_counter(event=None):
            text = goals_text.get('1.0', 'end-1c')
            remaining = 100 - len(text)
            char_counter.config(text=str(remaining))
            if remaining < 0:
                char_counter.config(fg=self.colors['high_priority'])
            else:
                char_counter.config(fg=self.colors['text_secondary'])
        
        goals_text.bind('<KeyRelease>', update_counter)
        
        def save_subject():
            data = {}
            for field, entry in entries.items():
                if field == 'goals':
                    data[field] = entry.get('1.0', 'end-1c').strip()
                else:
                    data[field] = entry.get().strip()
            
            if not data['code'] or not data['name']:
                messagebox.showerror("Error", "Subject Code and Name are required!")
                return
            
            if len(data['goals']) > 100:
                messagebox.showerror("Error", "Goals must be 100 characters or less!")
                return
            
            try:
                units = int(data['units']) if data['units'] else 0
            except ValueError:
                messagebox.showerror("Error", "Units must be a number!")
                return
            
            try:
                self.db.add_subject(data['code'], data['name'], data['instructor'], units, data['goals'])
                self.show_toast("Subject added successfully!")
                dialog.destroy()
                self.load_subjects_data()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Subject code already exists!")
        
        button_frame = tk.Frame(dialog, bg=self.colors['soft_pink'], pady=20)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="💾 Save Subject", 
                  command=save_subject, style='Primary.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=dialog.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def edit_subject_dialog(self):
        """Dialog for editing a subject with Goals character limit"""
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to edit!")
            return
        
        subject_data = self.subjects_tree.item(selected[0])['values']
        old_code = subject_data[0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Subject")
        dialog.geometry("650x550")
        dialog.configure(bg=self.colors['soft_pink'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        header = tk.Label(dialog,
                         text="Edit Subject",
                         font=self.fonts['subheader'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'],
                         pady=20)
        header.pack(fill='x')
        
        form_frame = tk.Frame(dialog, bg=self.colors['card_bg'], padx=40, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        fields = [
            ("Subject Code:", "code"),
            ("Subject Name:", "name"),
            ("Instructor:", "instructor"),
            ("Units:", "units"),
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label, 
                    bg=self.colors['card_bg'],
                    font=self.fonts['small']).grid(row=i, column=0, sticky='e', pady=15, padx=(0, 20))
            
            entry = tk.Entry(form_frame, width=35, font=self.fonts['small'],
                            bg=self.colors['accent_light'])
            entry.insert(0, str(subject_data[i] or ''))
            entry.grid(row=i, column=1, pady=15, sticky='w')
            entries[field] = entry
        
        # Goals with character counter
        tk.Label(form_frame, text="Goals (max 100 chars):", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=4, column=0, sticky='ne', pady=15, padx=(0, 20))
        
        goals_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        goals_frame.grid(row=4, column=1, pady=15, sticky='w')
        
        goals_text = tk.Text(goals_frame, height=5, width=35, font=self.fonts['small'],
                            bg=self.colors['accent_light'])
        goals_text.insert('1.0', subject_data[4] or '')
        goals_text.pack(side='left')
        entries['goals'] = goals_text
        
        # Character counter
        remaining = 100 - len(subject_data[4] or '')
        char_counter = tk.Label(goals_frame, text=str(remaining), 
                               bg=self.colors['card_bg'], font=self.fonts['small'],
                               fg=self.colors['text_secondary'])
        char_counter.pack(side='left', padx=10)
        
        def update_counter(event=None):
            text = goals_text.get('1.0', 'end-1c')
            remaining = 100 - len(text)
            char_counter.config(text=str(remaining))
            if remaining < 0:
                char_counter.config(fg=self.colors['high_priority'])
            else:
                char_counter.config(fg=self.colors['text_secondary'])
        
        goals_text.bind('<KeyRelease>', update_counter)
        
        def update_subject():
            data = {}
            for field, entry in entries.items():
                if field == 'goals':
                    data[field] = entry.get('1.0', 'end-1c').strip()
                else:
                    data[field] = entry.get().strip()
            
            if not data['code'] or not data['name']:
                messagebox.showerror("Error", "Subject Code and Name are required!")
                return
            
            if len(data['goals']) > 100:
                messagebox.showerror("Error", "Goals must be 100 characters or less!")
                return
            
            try:
                units = int(data['units']) if data['units'] else 0
            except ValueError:
                messagebox.showerror("Error", "Units must be a number!")
                return
            
            try:
                success = self.db.update_subject(old_code, data['code'], data['name'], 
                                               data['instructor'], units, data['goals'])
                if success:
                    self.show_toast("Subject updated successfully!")
                    dialog.destroy()
                    self.load_subjects_data()
                else:
                    messagebox.showerror("Error", "Subject code already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        button_frame = tk.Frame(dialog, bg=self.colors['soft_pink'], pady=20)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="💾 Update Subject", 
                  command=update_subject, style='Primary.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=dialog.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def delete_subject(self):
        """Delete selected subject using SubjectCode"""
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete!")
            return
        
        subject_data = self.subjects_tree.item(selected[0])['values']
        subject_code = subject_data[0]
        
        # Database method shows confirmation dialog
        if self.db.delete_subject(subject_code):
            self.show_toast("Subject deleted successfully!")
            self.load_subjects_data()
    
    def show_tasks(self):
        """Show tasks management page - SIMPLE CRUD INTERFACE"""
        self.clear_content()
        self.set_active_nav("✔ Tasks")
        
        # Header
        header = tk.Label(self.content_frame,
                         text="✔ Tasks Management",
                         font=self.fonts['header'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'])
        header.pack(pady=(0, 25))
        
        # Control frame with CRUD buttons and filter
        control_frame = tk.Frame(self.content_frame, bg=self.colors['soft_pink'])
        control_frame.pack(fill='x', pady=(0, 20))
        
        # CRUD buttons
        ttk.Button(control_frame, text="+ Create Task", 
                  command=self.create_task, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="✏️ Edit Task", 
                  command=self.edit_task, style='Secondary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="🗑️ Delete Task", 
                  command=self.delete_task, style='Secondary.TButton').pack(side='left', padx=5)
        
        # Filter by subject
        tk.Label(control_frame, text="Filter by Subject:", 
                bg=self.colors['soft_pink'], font=self.fonts['small']).pack(side='left', padx=(30, 10))
        
        self.task_filter_var = tk.StringVar(value="All Subjects")
        self.task_filter_combo = ttk.Combobox(control_frame, textvariable=self.task_filter_var, 
                                             state='readonly', width=30)
        self.task_filter_combo.pack(side='left')
        self.task_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_tasks_table())
        
        # Load subjects for filter
        self.load_task_filter_options()
        
        # Tasks table
        self.create_tasks_table()
    
    def load_task_filter_options(self):
        """Load subjects into filter dropdown"""
        subjects = self.db.get_subjects()
        options = ["All Subjects"] + [f"{code} - {name}" for code, name, *_ in subjects]
        self.task_filter_combo['values'] = options
    
    def create_tasks_table(self):
        """Create tasks table with Treeview - SIMPLE DESIGN"""
        table_container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        table_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('ID', 'Subject', 'Task Name', 'Deadline', 'Priority', 'Status')
        self.tasks_tree = ttk.Treeview(table_container, columns=columns, show='headings', 
                                      height=15, style='Pastel.Treeview')
        
        # Configure columns
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=100, stretch=True)
        
        # Set specific widths
        self.tasks_tree.column('ID', width=50)
        self.tasks_tree.column('Subject', width=150)
        self.tasks_tree.column('Task Name', width=300)
        self.tasks_tree.column('Deadline', width=100)
        self.tasks_tree.column('Priority', width=100)
        self.tasks_tree.column('Status', width=120)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_container, orient='vertical', command=self.tasks_tree.yview)
        hsb = ttk.Scrollbar(table_container, orient='horizontal', command=self.tasks_tree.xview)
        self.tasks_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tasks_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew', columnspan=2)
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Load data
        self.refresh_tasks_table()
    
    def refresh_tasks_table(self):
        """Refresh tasks table with current filter"""
        # Clear existing data
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        # Get filter
        filter_value = self.task_filter_var.get()
        
        if filter_value == "All Subjects":
            tasks = self.db.get_tasks()
        else:
            subject_code = filter_value.split(' - ')[0]
            tasks = self.db.get_tasks(subject_code)
        
        # Store mapping of tree item IDs to database TaskIDs
        self.task_id_mapping = {}
        
        # Insert tasks into treeview
        for i, task in enumerate(tasks):
            task_id = task[0]  # TaskID from database
            subject_code = task[1]  # SubjectCode
            task_name = task[2]  # TaskName
            deadline = task[3]  # Deadline
            priority = task[4]  # Priority
            status = task[5]  # Status
            subject_name = task[6]  # Subject Name from join
            
            # Determine tag for coloring
            tag = 'high' if priority == 'High' else 'medium' if priority == 'Medium' else 'low'
            if status == 'Completed':
                tag = 'completed'
            elif deadline and datetime.strptime(deadline, '%Y-%m-%d').date() < date.today() and status != 'Completed':
                tag = 'overdue'
            
            values = (task_id, f"{subject_code} - {subject_name}", task_name, deadline, priority, status)
            item_id = self.tasks_tree.insert('', 'end', values=values, tags=(tag,))
            
            # Store mapping
            self.task_id_mapping[item_id] = task_id
        
        # Configure tag colors
        self.tasks_tree.tag_configure('high', foreground=self.colors['high_priority'])
        self.tasks_tree.tag_configure('medium', foreground=self.colors['medium_priority'])
        self.tasks_tree.tag_configure('low', foreground=self.colors['low_priority'])
        self.tasks_tree.tag_configure('completed', foreground=self.colors['success'])
        self.tasks_tree.tag_configure('overdue', foreground=self.colors['high_priority'], background='#FFE6E6')
    
    def create_task(self):
        """Create a new task - opens form dialog"""
        self.task_form_dialog("Create New Task")
    
    def edit_task(self):
        """Edit selected task"""
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        
        # Get task ID from mapping
        item_id = selected[0]
        if item_id not in self.task_id_mapping:
            messagebox.showerror("Error", "Could not find task data!")
            return
        
        task_id = self.task_id_mapping[item_id]
        
        # Get task details from tree
        task_data = self.tasks_tree.item(item_id)['values']
        
        # Open edit dialog
        self.task_form_dialog("Edit Task", task_id=task_id, task_data=task_data)
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        # Get task ID from mapping
        item_id = selected[0]
        if item_id not in self.task_id_mapping:
            messagebox.showerror("Error", "Could not find task data!")
            return
        
        task_id = self.task_id_mapping[item_id]
        task_name = self.tasks_tree.item(item_id)['values'][2]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete task:\n\n'{task_name}'?"):
            try:
                self.db.delete_task(task_id)
                self.show_toast("Task deleted successfully!")
                self.refresh_tasks_table()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")
    
    def task_form_dialog(self, title, task_id=None, task_data=None):
        """Task form dialog for both create and edit"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x500")
        dialog.configure(bg=self.colors['soft_pink'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = tk.Label(dialog,
                         text=title,
                         font=self.fonts['subheader'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'],
                         pady=15)
        header.pack(fill='x')
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.colors['card_bg'], padx=30, pady=20)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Subject selection
        tk.Label(form_frame, text="Subject:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=0, column=0, sticky='e', pady=10, padx=(0, 10))
        subject_combo = ttk.Combobox(form_frame, state='readonly', width=30)
        subject_combo.grid(row=0, column=1, pady=10, sticky='w')
        
        # Task name
        tk.Label(form_frame, text="Task Name:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=1, column=0, sticky='e', pady=10, padx=(0, 10))
        task_name_entry = tk.Entry(form_frame, width=33, font=self.fonts['small'],
                                  bg=self.colors['accent_light'])
        task_name_entry.grid(row=1, column=1, pady=10, sticky='w')
        
        # Deadline
        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=2, column=0, sticky='e', pady=10, padx=(0, 10))
        deadline_entry = tk.Entry(form_frame, width=33, font=self.fonts['small'],
                                 bg=self.colors['accent_light'])
        deadline_entry.grid(row=2, column=1, pady=10, sticky='w')
        
        # Priority
        tk.Label(form_frame, text="Priority:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=3, column=0, sticky='e', pady=10, padx=(0, 10))
        priority_combo = ttk.Combobox(form_frame, values=['High', 'Medium', 'Low'], state='readonly', width=30)
        priority_combo.grid(row=3, column=1, pady=10, sticky='w')
        
        # Status
        tk.Label(form_frame, text="Status:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=4, column=0, sticky='e', pady=10, padx=(0, 10))
        status_combo = ttk.Combobox(form_frame, values=['Not Started', 'In Progress', 'Completed'], state='readonly', width=30)
        status_combo.grid(row=4, column=1, pady=10, sticky='w')
        
        # Load subjects
        subjects = self.db.get_subjects()
        subject_options = [f"{code} - {name}" for code, name, *_ in subjects]
        subject_combo['values'] = subject_options
        
        # Set default values
        priority_combo.set('Medium')
        status_combo.set('Not Started')
        
        # If editing, pre-fill form
        if task_data:
            # Extract subject from task_data (format: "CS 211 - Object-Oriented Programming")
            subject_display = task_data[1]
            subject_combo.set(subject_display)
            task_name_entry.insert(0, task_data[2])
            deadline_entry.insert(0, task_data[3])
            priority_combo.set(task_data[4])
            status_combo.set(task_data[5])
        
        def save_task():
            # Validate inputs
            subject = subject_combo.get()
            task_name = task_name_entry.get().strip()
            deadline = deadline_entry.get().strip()
            priority = priority_combo.get()
            status = status_combo.get()
            
            if not subject:
                messagebox.showerror("Error", "Please select a subject!")
                return
            
            if not task_name:
                messagebox.showerror("Error", "Task name is required!")
                return
            
            if not deadline:
                messagebox.showerror("Error", "Deadline is required!")
                return
            
            # Validate deadline format
            try:
                datetime.strptime(deadline, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format!")
                return
            
            # Extract subject code
            subject_code = subject.split(' - ')[0]
            
            try:
                if task_id:  # Update existing task
                    self.db.update_task(task_id, subject_code, task_name, deadline, priority, status)
                    self.show_toast("Task updated successfully!")
                else:  # Create new task
                    self.db.add_task(subject_code, task_name, deadline, priority, status)
                    self.show_toast("Task created successfully!")
                
                dialog.destroy()
                self.refresh_tasks_table()
                
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {str(e)}")
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.colors['soft_pink'], pady=15)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="💾 Save", 
                  command=save_task, style='Primary.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=dialog.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def show_schedule(self):
        """Show schedule page using SubjectCode"""
        self.clear_content()
        self.set_active_nav("🕒 Schedule")
        
        header = tk.Label(self.content_frame,
                         text="🕒 Weekly Schedule",
                         font=self.fonts['header'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'])
        header.pack(pady=(0, 25))
        
        # Control frame
        control_frame = tk.Frame(self.content_frame, bg=self.colors['soft_pink'])
        control_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Button(control_frame, text="+ Add Schedule Entry",
                  command=self.add_schedule_dialog, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="🗑️ Delete Selected Entry",
                  command=self.delete_schedule_entry, style='Secondary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="✏️ Edit Selected Entry",
                  command=self.edit_schedule_entry_dialog, style='Secondary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="🔄 Refresh Schedule",
                  command=self.load_schedule_data, style='Secondary.TButton').pack(side='left', padx=5)
        
        # Schedule grid - FULL WIDTH
        self.create_schedule_grid()
    
    def create_schedule_grid(self):
        """Create weekly schedule grid (7 days x 8 time slots) showing SubjectCode - FULL WIDTH"""
        grid_container = tk.Frame(self.content_frame, bg=self.colors['card_bg'], padx=10, pady=10)
        grid_container.pack(fill='both', expand=True)
        
        # Day headers - WIDER
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            header = tk.Frame(grid_container, bg=self.colors['dusty_pink'], height=50, width=200)
            header.grid(row=0, column=i+1, sticky='nsew', padx=1, pady=1)
            header.grid_propagate(False)
            
            label = tk.Label(header, text=day, font=self.fonts['normal'],
                            bg=self.colors['dusty_pink'], fg='white')
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Time slots (8 slots from 7:00 to 15:00) - TALLER
        time_slots = [
            '07:00-08:00', '08:00-09:00', '09:00-10:00', '10:00-11:00',
            '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00'
        ]
        
        self.schedule_cells = {}
        self.schedule_labels = {}  # Store labels for delete functionality
        self.schedule_entries = {}  # Store entry data
        
        for row, time_slot in enumerate(time_slots):
            # Time label
            time_label = tk.Frame(grid_container, bg=self.colors['accent_light'], height=100, width=100)
            time_label.grid(row=row+1, column=0, sticky='nsew', padx=1, pady=1)
            time_label.grid_propagate(False)
            
            label = tk.Label(time_label, text=time_slot, font=self.fonts['small'],
                            bg=self.colors['accent_light'], fg=self.colors['text_primary'])
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Day cells - WIDER AND TALLER
            for col, day in enumerate(days):
                cell = tk.Frame(grid_container, bg=self.colors['card_bg'], height=100, width=200,
                               relief='ridge', borderwidth=1)
                cell.grid(row=row+1, column=col+1, sticky='nsew', padx=1, pady=1)
                cell.grid_propagate(False)
                
                # Store cell reference
                cell_id = f"{day}_{time_slot}"
                self.schedule_cells[cell_id] = cell
                
                # Bind click event to add schedule
                cell.bind('<Button-1>', lambda e, d=day, t=time_slot: self.on_schedule_cell_click(d, t))
        
        # Configure grid weights
        grid_container.grid_columnconfigure(0, weight=0)
        for i in range(1, len(days) + 1):
            grid_container.grid_columnconfigure(i, weight=1)
        for i in range(len(time_slots) + 1):
            grid_container.grid_rowconfigure(i, weight=1)
        
        # Load schedule data
        self.load_schedule_data()
    
    def load_schedule_data(self):
        """Load schedule data into grid showing SubjectCode"""
        # Clear all cells first
        for cell in self.schedule_cells.values():
            for widget in cell.winfo_children():
                widget.destroy()
        
        self.schedule_labels.clear()  # Clear old labels
        self.schedule_entries.clear()  # Clear old entries
        
        # Load schedule entries using SubjectCode
        schedule_entries = self.db.get_schedule()
        
        for entry in schedule_entries:
            schedule_id = entry[0]
            day = entry[2]
            start_time = entry[3]
            end_time = entry[4]
            subject_code = entry[1]
            subject_name = entry[6]
            room = entry[5] or ''
            
            # Find matching time slot
            for time_slot in self.schedule_cells.keys():
                slot_day, slot_range = time_slot.split('_')
                if day == slot_day:
                    slot_start, slot_end = slot_range.split('-')
                    slot_start_hour = int(slot_start.split(':')[0])
                    start_hour = int(start_time.split(':')[0])
                    
                    # Check if start time falls within this slot
                    if slot_start_hour <= start_hour < slot_start_hour + 1:
                        cell = self.schedule_cells[time_slot]
                        
                        # Create entry label - shows SubjectCode
                        entry_text = f"{subject_code}\n{start_time}-{end_time}"
                        if room:
                            entry_text += f"\n{room}"
                        
                        label = tk.Label(cell, text=entry_text, font=self.fonts['small'],
                                        bg=self.colors['soft_pink'], fg=self.colors['text_primary'],
                                        wraplength=180, justify='center', cursor="hand2")
                        label.pack(fill='both', expand=True, padx=2, pady=2)
                        
                        # Store ScheduleID in label object
                        label.schedule_id = schedule_id
                        
                        # Bind click to select
                        label.bind('<Button-1>', lambda e, sid=schedule_id: self.select_schedule_entry(sid))
                        
                        # Store references
                        self.schedule_labels[schedule_id] = label
                        self.schedule_entries[schedule_id] = {
                            'day': day,
                            'start_time': start_time,
                            'end_time': end_time,
                            'subject_code': subject_code,
                            'room': room,
                            'cell': time_slot
                        }
                        break
    
    def on_schedule_cell_click(self, day, time_slot):
        """Handle schedule cell click"""
        start_time = time_slot.split('-')[0] + ':00'
        
        self.add_schedule_dialog(day, start_time)
    
    def select_schedule_entry(self, schedule_id):
        """Select a schedule entry (for deletion/editing)"""
        # Clear previous selection
        for sid, label in self.schedule_labels.items():
            label.config(bg=self.colors['soft_pink'])
        
        # Highlight selected
        if schedule_id in self.schedule_labels:
            self.schedule_labels[schedule_id].config(bg=self.colors['hover'])
            self.selected_schedule_id = schedule_id
    
    def delete_schedule_entry(self):
        """Delete selected schedule entry"""
        if not hasattr(self, 'selected_schedule_id'):
            messagebox.showwarning("Warning", "Please select a schedule entry to delete!")
            return
        
        schedule_id = self.selected_schedule_id
        
        if schedule_id in self.schedule_entries:
            entry = self.schedule_entries[schedule_id]
            description = f"{entry['subject_code']} ({entry['start_time']}-{entry['end_time']}) on {entry['day']}"
            
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete schedule entry:\n\n{description}\n\nAre you sure?"):
                self.db.delete_schedule(schedule_id)
                self.show_toast("Schedule entry deleted successfully!")
                self.load_schedule_data()
                delattr(self, 'selected_schedule_id')
    
    def edit_schedule_entry_dialog(self):
        """Edit selected schedule entry"""
        if not hasattr(self, 'selected_schedule_id'):
            messagebox.showwarning("Warning", "Please select a schedule entry to edit!")
            return
        
        schedule_id = self.selected_schedule_id
        
        if schedule_id not in self.schedule_entries:
            return
        
        # Get entry details
        schedule_entries = self.db.get_schedule()
        entry = None
        for e in schedule_entries:
            if e[0] == schedule_id:
                entry = e
                break
        
        if not entry:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Schedule Entry")
        dialog.geometry("600x550")
        dialog.configure(bg=self.colors['soft_pink'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        header = tk.Label(dialog,
                         text="Edit Schedule Entry",
                         font=self.fonts['subheader'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'],
                         pady=20)
        header.pack(fill='x')
        
        form_frame = tk.Frame(dialog, bg=self.colors['card_bg'], padx=40, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Subject - shows SubjectCode
        tk.Label(form_frame, text="Subject:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=0, column=0, sticky='e', pady=15, padx=(0, 20))
        subject_combo = ttk.Combobox(form_frame, state='readonly', width=33)
        subject_combo.grid(row=0, column=1, pady=15, sticky='w')
        
        # Day
        tk.Label(form_frame, text="Day:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=1, column=0, sticky='e', pady=15, padx=(0, 20))
        day_combo = ttk.Combobox(form_frame, values=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 
                                state='readonly', width=33)
        day_combo.grid(row=1, column=1, pady=15, sticky='w')
        
        # Start time
        tk.Label(form_frame, text="Start Time:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=2, column=0, sticky='e', pady=15, padx=(0, 20))
        time_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        time_frame.grid(row=2, column=1, pady=15, sticky='w')
        
        start_hour = ttk.Combobox(time_frame, values=[f"{h:02d}" for h in range(7, 17)], width=6, state='readonly')
        start_hour.pack(side='left')
        tk.Label(time_frame, text=":", bg=self.colors['card_bg'], font=self.fonts['small']).pack(side='left')
        start_min = ttk.Combobox(time_frame, values=['00', '15', '30', '45'], width=6, state='readonly')
        start_min.pack(side='left')
        
        # End time
        tk.Label(form_frame, text="End Time:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=3, column=0, sticky='e', pady=15, padx=(0, 20))
        time_frame_end = tk.Frame(form_frame, bg=self.colors['card_bg'])
        time_frame_end.grid(row=3, column=1, pady=15, sticky='w')
        
        end_hour = ttk.Combobox(time_frame_end, values=[f"{h:02d}" for h in range(7, 18)], width=6, state='readonly')
        end_hour.pack(side='left')
        tk.Label(time_frame_end, text=":", bg=self.colors['card_bg'], font=self.fonts['small']).pack(side='left')
        end_min = ttk.Combobox(time_frame_end, values=['00', '15', '30', '45'], width=6, state='readonly')
        end_min.pack(side='left')
        
        # Room
        tk.Label(form_frame, text="Room:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=4, column=0, sticky='e', pady=15, padx=(0, 20))
        room = tk.Entry(form_frame, width=35, font=self.fonts['small'],
                       bg=self.colors['accent_light'])
        room.grid(row=4, column=1, pady=15, sticky='w')
        
        # Load subjects using SubjectCode
        subjects = self.db.get_subjects()
        subject_options = [f"{code} - {name}" for code, name, *_ in subjects]
        subject_combo['values'] = subject_options
        
        # Set current values
        day_combo.set(entry[2])
        
        start_h, start_m = entry[3].split(':')
        start_hour.set(start_h)
        start_min.set(start_m)
        
        end_h, end_m = entry[4].split(':')
        end_hour.set(end_h)
        end_min.set(end_m)
        
        room.insert(0, entry[5] or '')
        
        # Set current subject
        current_subject_code = entry[1]
        for option in subject_options:
            if current_subject_code in option:
                subject_combo.set(option)
                break
        
        def update_schedule():
            subject_selection = subject_combo.get()
            if not subject_selection:
                messagebox.showerror("Error", "Please select a subject!")
                return
            
            subject_code = subject_selection.split(' - ')[0]
            
            if not day_combo.get() or not start_hour.get() or not end_hour.get():
                messagebox.showerror("Error", "Day and times are required!")
                return
            
            start_time = f"{start_hour.get()}:{start_min.get()}"
            end_time = f"{end_hour.get()}:{end_min.get()}"
            
            try:
                # Validate times
                datetime.strptime(start_time, '%H:%M')
                datetime.strptime(end_time, '%H:%M')
                
                # Check if end time is after start time
                start_dt = datetime.strptime(start_time, '%H:%M')
                end_dt = datetime.strptime(end_time, '%H:%M')
                if end_dt <= start_dt:
                    messagebox.showerror("Error", "End time must be after start time!")
                    return
                
                self.db.update_schedule(schedule_id, subject_code, day_combo.get(), start_time, 
                                       end_time, room.get())
                self.show_toast("Schedule entry updated successfully!")
                dialog.destroy()
                self.load_schedule_data()
                delattr(self, 'selected_schedule_id')
            except ValueError:
                messagebox.showerror("Error", "Invalid time format! Use HH:MM")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        button_frame = tk.Frame(dialog, bg=self.colors['soft_pink'], pady=20)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="💾 Update Entry", 
                  command=update_schedule, style='Primary.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=dialog.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def add_schedule_dialog(self, default_day=None, default_start=None):
        """Dialog for adding schedule entry using SubjectCode as FK"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Schedule Entry")
        dialog.geometry("600x550")
        dialog.configure(bg=self.colors['soft_pink'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        header = tk.Label(dialog,
                         text="Add Schedule Entry",
                         font=self.fonts['subheader'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'],
                         pady=20)
        header.pack(fill='x')
        
        form_frame = tk.Frame(dialog, bg=self.colors['card_bg'], padx=40, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Subject - shows SubjectCode
        tk.Label(form_frame, text="Subject:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=0, column=0, sticky='e', pady=15, padx=(0, 20))
        subject_combo = ttk.Combobox(form_frame, state='readonly', width=33)
        subject_combo.grid(row=0, column=1, pady=15, sticky='w')
        
        # Day
        tk.Label(form_frame, text="Day:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=1, column=0, sticky='e', pady=15, padx=(0, 20))
        day_combo = ttk.Combobox(form_frame, values=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 
                                state='readonly', width=33)
        day_combo.grid(row=1, column=1, pady=15, sticky='w')
        
        # Start time
        tk.Label(form_frame, text="Start Time:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=2, column=0, sticky='e', pady=15, padx=(0, 20))
        time_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        time_frame.grid(row=2, column=1, pady=15, sticky='w')
        
        start_hour = ttk.Combobox(time_frame, values=[f"{h:02d}" for h in range(7, 17)], width=6, state='readonly')
        start_hour.pack(side='left')
        tk.Label(time_frame, text=":", bg=self.colors['card_bg'], font=self.fonts['small']).pack(side='left')
        start_min = ttk.Combobox(time_frame, values=['00', '15', '30', '45'], width=6, state='readonly')
        start_min.pack(side='left')
        
        # End time
        tk.Label(form_frame, text="End Time:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=3, column=0, sticky='e', pady=15, padx=(0, 20))
        time_frame_end = tk.Frame(form_frame, bg=self.colors['card_bg'])
        time_frame_end.grid(row=3, column=1, pady=15, sticky='w')
        
        end_hour = ttk.Combobox(time_frame_end, values=[f"{h:02d}" for h in range(7, 18)], width=6, state='readonly')
        end_hour.pack(side='left')
        tk.Label(time_frame_end, text=":", bg=self.colors['card_bg'], font=self.fonts['small']).pack(side='left')
        end_min = ttk.Combobox(time_frame_end, values=['00', '15', '30', '45'], width=6, state='readonly')
        end_min.pack(side='left')
        
        # Room
        tk.Label(form_frame, text="Room:", 
                bg=self.colors['card_bg'], font=self.fonts['small']).grid(row=4, column=0, sticky='e', pady=15, padx=(0, 20))
        room = tk.Entry(form_frame, width=35, font=self.fonts['small'],
                       bg=self.colors['accent_light'])
        room.grid(row=4, column=1, pady=15, sticky='w')
        
        # Load subjects using SubjectCode
        subjects = self.db.get_subjects()
        subject_options = [f"{code} - {name}" for code, name, *_ in subjects]
        subject_combo['values'] = subject_options
        if subject_options:
            subject_combo.set(subject_options[0])
        
        # Set defaults if provided
        if default_day:
            day_combo.set(default_day)
        else:
            day_combo.set('Mon')
        
        if default_start:
            hour, minute = default_start.split(':')
            start_hour.set(hour)
            start_min.set(minute)
            # Set end time as 1 hour later
            end_h = int(hour) + 1
            end_hour.set(f"{end_h:02d}")
            end_min.set(minute)
        else:
            start_hour.set('09')
            start_min.set('00')
            end_hour.set('10')
            end_min.set('00')
        
        def save_schedule():
            subject_selection = subject_combo.get()
            if not subject_selection:
                messagebox.showerror("Error", "Please select a subject!")
                return
            
            subject_code = subject_selection.split(' - ')[0]
            
            if not day_combo.get() or not start_hour.get() or not end_hour.get():
                messagebox.showerror("Error", "Day and times are required!")
                return
            
            start_time = f"{start_hour.get()}:{start_min.get()}"
            end_time = f"{end_hour.get()}:{end_min.get()}"
            
            try:
                # Validate times
                datetime.strptime(start_time, '%H:%M')
                datetime.strptime(end_time, '%H:%M')
                
                # Check if end time is after start time
                start_dt = datetime.strptime(start_time, '%H:%M')
                end_dt = datetime.strptime(end_time, '%H:%M')
                if end_dt <= start_dt:
                    messagebox.showerror("Error", "End time must be after start time!")
                    return
                
                self.db.add_schedule(subject_code, day_combo.get(), start_time, 
                                    end_time, room.get())
                self.show_toast("Schedule entry added successfully!")
                dialog.destroy()
                self.load_schedule_data()
            except ValueError:
                messagebox.showerror("Error", "Invalid time format! Use HH:MM")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        button_frame = tk.Frame(dialog, bg=self.colors['soft_pink'], pady=20)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="💾 Save Entry", 
                  command=save_schedule, style='Primary.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=dialog.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def show_records(self):
        """Show records/reports page with the requested 6 reports"""
        self.clear_content()
        self.set_active_nav("📁 Records")
        
        header = tk.Label(self.content_frame,
                         text="📁 Records & Reports",
                         font=self.fonts['header'],
                         bg=self.colors['soft_pink'],
                         fg=self.colors['deep_maroon'])
        header.pack(pady=(0, 25))
        
        # Report selection
        report_frame = tk.Frame(self.content_frame, bg=self.colors['soft_pink'])
        report_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(report_frame, text="Select Report:", 
                bg=self.colors['soft_pink'], font=self.fonts['small']).pack(side='left', padx=(0, 15))
        
        self.report_var = tk.StringVar()
        report_combo = ttk.Combobox(report_frame, textvariable=self.report_var, state='readonly', width=30)
        report_combo['values'] = [
            'All Subjects with Tasks',
            'Upcoming Tasks',
            'Tasks Today',
            'Completed Tasks',
            'Missing Tasks',
            'Schedule for Today'
        ]
        report_combo.set('All Subjects with Tasks')
        report_combo.pack(side='left', padx=(0, 25))
        
        ttk.Button(report_frame, text="📊 Generate Report", 
                  command=self.generate_report, style='Primary.TButton').pack(side='left')
        
        ttk.Button(report_frame, text="📄 Export to CSV", 
                  command=self.export_to_csv, style='Secondary.TButton').pack(side='left', padx=10)
        ttk.Button(report_frame, text="🔄 Refresh", 
                  command=self.generate_report, style='Secondary.TButton').pack(side='left', padx=10)
        
        # Results frame - FULL WIDTH
        self.results_frame = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Generate initial report
        self.generate_report()
    
    def generate_report(self):
        """Generate the selected report from the 6 requested filters"""
        report_type = self.report_var.get()
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Label(self.results_frame,
                         text=f"Report: {report_type}",
                         font=self.fonts['subheader'],
                         bg=self.colors['deep_crimson'],
                         fg='white',
                         pady=15)
        header.pack(fill='x')
        
        # Get data based on report type
        if report_type == 'All Subjects with Tasks':
            data = self.db.get_all_subjects_with_tasks()
            columns = ('SubjectCode', 'Name', 'Instructor', 'Units', 'Tasks')
        elif report_type == 'Upcoming Tasks':
            data = self.db.get_upcoming_tasks()
            columns = ('TaskName', 'Deadline', 'Priority', 'Status', 'SubjectCode', 'Name')
        elif report_type == 'Tasks Today':
            data = self.db.get_tasks_today()
            columns = ('TaskName', 'Deadline', 'Priority', 'Status', 'SubjectCode', 'Name')
        elif report_type == 'Completed Tasks':
            data = self.db.get_completed_tasks()
            columns = ('TaskName', 'Deadline', 'Priority', 'Status', 'SubjectCode', 'Name')
        elif report_type == 'Missing Tasks':
            data = self.db.get_missing_tasks()
            columns = ('TaskName', 'Deadline', 'Priority', 'Status', 'SubjectCode', 'Name')
        elif report_type == 'Schedule for Today':
            data = self.db.get_schedule_for_today()
            columns = ('SubjectCode', 'Name', 'StartTime', 'EndTime', 'Room')
        else:
            data = []
            columns = ()
        
        # Store for export
        self.current_report_data = (report_type, columns, data)
        
        # Create treeview with FULL WIDTH
        if data:
            tree_container = tk.Frame(self.results_frame, bg=self.colors['card_bg'])
            tree_container.pack(fill='both', expand=True)
            
            tree = ttk.Treeview(tree_container, columns=columns, show='headings', 
                               height=15, style='Pastel.Treeview')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=200, stretch=True)  # Full width
            
            # Add scrollbars
            vsb = ttk.Scrollbar(tree_container, orient='vertical', command=tree.yview)
            hsb = ttk.Scrollbar(tree_container, orient='horizontal', command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew', columnspan=2)
            
            tree_container.grid_rowconfigure(0, weight=1)
            tree_container.grid_columnconfigure(0, weight=1)
            
            # Insert data
            for i, row in enumerate(data):
                tag = 'even' if i % 2 == 0 else 'odd'
                tree.insert('', 'end', values=row, tags=(tag,))
            
            tree.tag_configure('even', background=self.colors['card_bg'])
            tree.tag_configure('odd', background=self.colors['accent_light'])
            
            # Show row count
            count_frame = tk.Frame(self.results_frame, bg=self.colors['card_bg'])
            count_frame.pack(fill='x', pady=5)
            
            count_label = tk.Label(count_frame,
                                  text=f"Total records: {len(data)}",
                                  font=self.fonts['small'],
                                  bg=self.colors['card_bg'],
                                  fg=self.colors['text_secondary'])
            count_label.pack()
        else:
            no_data = tk.Label(self.results_frame,
                              text="No data available for this report.",
                              font=self.fonts['normal'],
                              bg=self.colors['card_bg'],
                              fg=self.colors['text_secondary'])
            no_data.pack(expand=True, pady=50)
    
    def export_to_csv(self):
        """Export current report to CSV"""
        if not hasattr(self, 'current_report_data'):
            messagebox.showwarning("Warning", "No report to export!")
            return
        
        report_type, columns, data = self.current_report_data
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"ClassIFY_{report_type.replace(' ', '_')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([f"ClassIFY Report: {report_type}"])
                    writer.writerow([f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                    writer.writerow([])
                    writer.writerow(columns)
                    
                    for row in data:
                        writer.writerow(row)
                    
                    writer.writerow([])
                    writer.writerow([f"Total records: {len(data)}"])
                self.show_toast(f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.add_subject_dialog() if "📚 Subjects" in self.root.title() else None)
        self.root.bind('<Control-t>', lambda e: self.create_task() if "✔ Tasks" in self.root.title() else None)
        self.root.bind('<Control-s>', lambda e: self.add_schedule_dialog() if "🕒 Schedule" in self.root.title() else None)
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self.refresh_current_page())
    
    def refresh_current_page(self):
        """Refresh current page"""
        current_nav = None
        for text, btn in self.nav_buttons.items():
            if str(btn.cget('style')) == 'NavActive.TButton':
                current_nav = text
                break
        
        if current_nav == "🏠 Home":
            self.show_dashboard()
        elif current_nav == "📚 Subjects":
            self.show_subjects()
        elif current_nav == "✔ Tasks":
            self.show_tasks()
        elif current_nav == "🕒 Schedule":
            self.show_schedule()
        elif current_nav == "📁 Records":
            self.show_records()


def write_user_manual():
    """Write USER_Manual.txt file"""
    user_manual = """Class-i-fy User Manual
----------------------

How to run:
1. (Optional) Install calendar widget: pip install tkcalendar
2. Run the app: python3 ClassIFY.py

Files created:
- ClassIFY.db          : SQLite database file (persistent storage)
- ClassIFY_tables.sql  : CREATE TABLE statements for the schema
- ClassIFY_data.sql    : Sample INSERT statements (seed data)
- USER_Manual.txt      : This manual

Quick overview:
- Home/Dashboard: See today's classes, monthly calendar, today's to-dos, and subjects with goals.
- Subjects: Add/Edit/Delete subjects. Fields: SubjectCode, Name, Instructor, Units, Goals (max 100 chars)
- Tasks: Add tasks linked to SubjectCode. Fields: TaskName, SubjectCode, Deadline(YYYY-MM-DD), Priority, Status.
- Schedule: Weekly grid (Mon..Sun) for class schedule entries (SubjectCode, StartTime, EndTime, Room). Click cells to add, click entries to select for edit/delete.
- Records/Reports: Run pre-built reports (All Subjects with Tasks, Upcoming Tasks, Tasks Today, Completed Tasks, Missing Tasks, Schedule for Today). Export to CSV allowed.

Important notes:
- All tables persist between runs. Data is not dropped on startup.
- Sample data is inserted only when the subjects table is empty (first run).
- Goals field supports up to 100 characters. A character counter is shown in the UI.
- Deleting a subject cascades and removes related tasks and schedule entries.
- SubjectCode is used as the primary key for subjects and as a foreign key in tasks and schedule.
- Tasks use auto-increment TaskID for uniqueness (hidden from user).

Key SQL queries used in Reports:
1. All Subjects with Tasks: Shows all subjects with their associated tasks
2. Upcoming Tasks: Tasks due from tomorrow forward
3. Tasks Today: Tasks due today
4. Completed Tasks: All completed tasks
5. Missing Tasks: Overdue tasks not yet completed
6. Schedule for Today: Today's class schedule

Keyboard Shortcuts:
- Ctrl+N: Add new subject (when in Subjects page)
- Ctrl+T: Add new task (when in Tasks page)
- Ctrl+S: Add new schedule entry (when in Schedule page)
- Ctrl+Q: Quit application
- F5: Refresh current page

Schedule Management:
- Click empty cells to add schedule entries
- Click existing entries to select them (they will be highlighted)
- Use buttons to edit or delete selected entries

(see ClassIFY_tables.sql and ClassIFY_data.sql in project root)

Contact:
- If you encounter errors, check the console for printouts and ensure Python 3.8+ is installed.
"""
    
    try:
        with open('USER_Manual.txt', 'w', encoding='utf-8') as f:
            f.write(user_manual)
        print("✅ Generated USER_Manual.txt")
    except Exception as e:
        print(f"⚠️ Could not write USER_Manual.txt: {e}")


def main():
    """Main function"""
    print("=" * 60)
    print("ClassIFY - Student Organizer")
    print("Using SubjectCode as primary key for all subject relationships")
    print("No numeric IDs - all tables connected via SubjectCode")
    print("=" * 60)
    
    # Write user manual
    write_user_manual()
    
    # Create and run application
    root = tk.Tk()
    app = ClassifyApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
    
    # Cleanup
    if hasattr(app, 'db'):
        app.db.close()


if __name__ == "__main__":
    main()