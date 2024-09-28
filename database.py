import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Function to create the required tables
def create_tables(conn):
    cur = conn.cursor()
    
    # Create students table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT NOT NULL
    )
    ''')

    # Create instructors table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS instructors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT NOT NULL
    )
    ''')

    # Create courses table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        instructor_id TEXT,
        FOREIGN KEY (instructor_id) REFERENCES instructors (id)
    )
    ''')

    # Create registrations table (Join table for students and courses)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        student_id TEXT,
        course_id TEXT,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
    ''')

    conn.commit()

# Function to add a student
def add_student(conn, student_id, name, age, email):
    cur = conn.cursor()
    cur.execute("INSERT INTO students (id, name, age, email) VALUES (?, ?, ?, ?)", 
                (student_id, name, age, email))
    conn.commit()

# Function to add an instructor
def add_instructor(conn, instructor_id, name, age, email):
    cur = conn.cursor()
    cur.execute("INSERT INTO instructors (id, name, age, email) VALUES (?, ?, ?, ?)", 
                (instructor_id, name, age, email))
    conn.commit()

# Function to add a course
def add_course(conn, course_id, name, instructor_id):
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (id, name, instructor_id) VALUES (?, ?, ?)", 
                (course_id, name, instructor_id))
    conn.commit()

# Function to register a student for a course
def register_student_for_course(conn, student_id, course_id):
    cur = conn.cursor()
    cur.execute("INSERT INTO registrations (student_id, course_id) VALUES (?, ?)", 
                (student_id, course_id))
    conn.commit()

# Function to get all students
def get_all_students(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    return cur.fetchall()

# Function to get all instructors
def get_all_instructors(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructors")
    return cur.fetchall()

# Function to get all courses
def get_all_courses(conn):
    cur = conn.cursor()
    cur.execute('''SELECT c.id, c.name, i.name as instructor_name 
                   FROM courses c 
                   LEFT JOIN instructors i ON c.instructor_id = i.id''')
    return cur.fetchall()

# Function to delete a student
def delete_student(conn, student_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

# Function to delete a course
def delete_course(conn, course_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()

# Backup the database
def backup_database(conn, backup_file):
    with open(backup_file, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    print(f"Backup completed: {backup_file}")
