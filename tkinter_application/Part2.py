import tkinter as tk
from tkinter import Button, Frame, Menu, Toplevel, filedialog, messagebox, ttk
from typing import List

from Part1 import Course, DataManagement, Instructor, Student
from Part4 import Database


class SchoolManagementSystem(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.master.winfo_toplevel().title("School Management System")
        self.master.geometry("1000x700")

        self.database = Database()

        self.create_menu()

        self.create_main_buttons()

        self.create_tabs()

    def create_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

    def create_main_buttons(self):
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        self.button_add_student = Button(
            button_frame, text="Add Student", width=15, command=self.new_student_window
        )
        self.button_add_student.grid(row=0, column=0, padx=5)

        self.button_add_instructor = Button(
            button_frame, text="Add Instructor", width=15, command=self.new_instructor_window
        )
        self.button_add_instructor.grid(row=0, column=1, padx=5)

        self.button_add_course = Button(
            button_frame, text="Add Course", width=15, command=self.new_course_window
        )
        self.button_add_course.grid(row=0, column=2, padx=5)

        self.button_register_course = Button(
            button_frame, text="Register Course", width=15, command=self.register_course_window
        )
        self.button_register_course.grid(row=0, column=3, padx=5)

        self.button_assign_instructor = Button(
            button_frame,
            text="Assign Instructor",
            width=15,
            command=self.assign_instructor_window,
        )
        self.button_assign_instructor.grid(row=0, column=4, padx=5)

    def create_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_all_records = ttk.Frame(self.notebook)
        self.tab_students = ttk.Frame(self.notebook)
        self.tab_instructors = ttk.Frame(self.notebook)
        self.tab_courses = ttk.Frame(self.notebook)
        self.tab_registrations = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_all_records, text="All Records")
        self.notebook.add(self.tab_students, text="Students")
        self.notebook.add(self.tab_instructors, text="Instructors")
        self.notebook.add(self.tab_courses, text="Courses")
        self.notebook.add(self.tab_registrations, text="Registrations")

        self.create_all_records_tab()
        self.create_students_tab()
        self.create_instructors_tab()
        self.create_courses_tab()
        self.create_registrations_tab()

    def create_all_records_tab(self):
        frame = self.tab_all_records

        search_frame = Frame(frame)
        search_frame.pack(pady=5, anchor='w')

        tk.Label(search_frame, text="Search by Student ID/Name or Course ID/Name:").pack(side=tk.LEFT, padx=5)
        self.all_records_search_var = tk.StringVar()
        self.entry_all_records_search = tk.Entry(search_frame, textvariable=self.all_records_search_var, width=40)
        self.entry_all_records_search.pack(side=tk.LEFT, padx=5)
        self.button_all_records_search = Button(
            search_frame, text="Search", command=self.search_all_records
        )
        self.button_all_records_search.pack(side=tk.LEFT, padx=5)
        self.button_all_records_reset = Button(
            search_frame, text="Reset", command=self.reset_all_records_search
        )
        self.button_all_records_reset.pack(side=tk.LEFT, padx=5)

        columns = ("Student ID", "Student Name", "Course ID", "Course Name", "Instructor ID", "Instructor Name")
        self.tree_all_records = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_all_records.heading(col, text=col)
            self.tree_all_records.column(col, width=120, anchor='center')
        self.tree_all_records.pack(fill=tk.BOTH, expand=True)

        self.attach_context_menu(self.tree_all_records, 'all_records')

        self.populate_all_records()

    def create_students_tab(self):
        frame = self.tab_students

        search_frame = Frame(frame)
        search_frame.pack(pady=5, anchor='w')

        tk.Label(search_frame, text="Search by ID or Name:").pack(side=tk.LEFT, padx=5)
        self.students_search_var = tk.StringVar()
        self.entry_students_search = tk.Entry(search_frame, textvariable=self.students_search_var, width=30)
        self.entry_students_search.pack(side=tk.LEFT, padx=5)
        self.button_students_search = Button(
            search_frame, text="Search", command=self.search_students
        )
        self.button_students_search.pack(side=tk.LEFT, padx=5)
        self.button_students_reset = Button(
            search_frame, text="Reset", command=self.reset_students_search
        )
        self.button_students_reset.pack(side=tk.LEFT, padx=5)

        columns = ("Student ID", "Name", "Age", "Email")
        self.tree_students = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_students.heading(col, text=col)
            self.tree_students.column(col, width=150, anchor='center')
        self.tree_students.pack(fill=tk.BOTH, expand=True)

        self.attach_context_menu(self.tree_students, 'students')

        self.populate_students()

    def create_instructors_tab(self):
        frame = self.tab_instructors

        search_frame = Frame(frame)
        search_frame.pack(pady=5, anchor='w')

        tk.Label(search_frame, text="Search by ID or Name:").pack(side=tk.LEFT, padx=5)
        self.instructors_search_var = tk.StringVar()
        self.entry_instructors_search = tk.Entry(search_frame, textvariable=self.instructors_search_var, width=30)
        self.entry_instructors_search.pack(side=tk.LEFT, padx=5)
        self.button_instructors_search = Button(
            search_frame, text="Search", command=self.search_instructors
        )
        self.button_instructors_search.pack(side=tk.LEFT, padx=5)
        self.button_instructors_reset = Button(
            search_frame, text="Reset", command=self.reset_instructors_search
        )
        self.button_instructors_reset.pack(side=tk.LEFT, padx=5)

        columns = ("Instructor ID", "Name", "Age", "Email")
        self.tree_instructors = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_instructors.heading(col, text=col)
            self.tree_instructors.column(col, width=150, anchor='center')
        self.tree_instructors.pack(fill=tk.BOTH, expand=True)

        self.attach_context_menu(self.tree_instructors, 'instructors')

        self.populate_instructors()

    def create_courses_tab(self):
        frame = self.tab_courses

        search_frame = Frame(frame)
        search_frame.pack(pady=5, anchor='w')

        tk.Label(search_frame, text="Search by ID or Name:").pack(side=tk.LEFT, padx=5)
        self.courses_search_var = tk.StringVar()
        self.entry_courses_search = tk.Entry(search_frame, textvariable=self.courses_search_var, width=30)
        self.entry_courses_search.pack(side=tk.LEFT, padx=5)
        self.button_courses_search = Button(
            search_frame, text="Search", command=self.search_courses
        )
        self.button_courses_search.pack(side=tk.LEFT, padx=5)
        self.button_courses_reset = Button(
            search_frame, text="Reset", command=self.reset_courses_search
        )
        self.button_courses_reset.pack(side=tk.LEFT, padx=5)

        columns = ("Course ID", "Course Name", "Instructor ID", "Instructor Name")
        self.tree_courses = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_courses.heading(col, text=col)
            self.tree_courses.column(col, width=150, anchor='center')
        self.tree_courses.pack(fill=tk.BOTH, expand=True)

        self.attach_context_menu(self.tree_courses, 'courses')

        self.populate_courses()

    def create_registrations_tab(self):
        frame = self.tab_registrations

        search_frame = Frame(frame)
        search_frame.pack(pady=5, anchor='w')

        tk.Label(search_frame, text="Search by Student ID/Name or Course ID/Name:").pack(side=tk.LEFT, padx=5)
        self.registrations_search_var = tk.StringVar()
        self.entry_registrations_search = tk.Entry(search_frame, textvariable=self.registrations_search_var, width=40)
        self.entry_registrations_search.pack(side=tk.LEFT, padx=5)
        self.button_registrations_search = Button(
            search_frame, text="Search", command=self.search_registrations
        )
        self.button_registrations_search.pack(side=tk.LEFT, padx=5)
        self.button_registrations_reset = Button(
            search_frame, text="Reset", command=self.reset_registrations_search
        )
        self.button_registrations_reset.pack(side=tk.LEFT, padx=5)

        columns = ("Registration ID", "Student ID", "Student Name", "Course ID", "Course Name")
        self.tree_registrations = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_registrations.heading(col, text=col)
            self.tree_registrations.column(col, width=120, anchor='center')
        self.tree_registrations.pack(fill=tk.BOTH, expand=True)

        self.attach_context_menu(self.tree_registrations, 'registrations')

        self.populate_registrations()

    def populate_all_records(self):
        for row in self.tree_all_records.get_children():
            self.tree_all_records.delete(row)

        self.database.cursor.execute(
            """
            SELECT 
                s.student_id, s.name, 
                c.course_id, c.course_name,
                i.instructor_id, i.name
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            """
        )
        records = self.database.cursor.fetchall()
        for record in records:
            self.tree_all_records.insert("", tk.END, values=record)

    def populate_students(self):
        for row in self.tree_students.get_children():
            self.tree_students.delete(row)

        students = self.database.get_students()
        for student in students:
            self.tree_students.insert("", tk.END, values=student)

    def populate_instructors(self):
        for row in self.tree_instructors.get_children():
            self.tree_instructors.delete(row)

        instructors = self.database.get_instructors()
        for instructor in instructors:
            self.tree_instructors.insert("", tk.END, values=instructor)

    def populate_courses(self):
        for row in self.tree_courses.get_children():
            self.tree_courses.delete(row)

        courses = self.database.get_courses()
        for course in courses:
            if course[2]:
                instructor_record = self.database.get_instructor_by_id(course[2])
                instructor_name = instructor_record[1] if instructor_record else "N/A"
            else:
                instructor_name = "N/A"
            self.tree_courses.insert("", tk.END, values=(course[0], course[1], course[2] if course[2] else "N/A", instructor_name))

    def populate_registrations(self):
        for row in self.tree_registrations.get_children():
            self.tree_registrations.delete(row)

        self.database.cursor.execute(
            """
            SELECT 
                r.id, 
                s.student_id, s.name, 
                c.course_id, c.course_name
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            """
        )
        records = self.database.cursor.fetchall()
        for record in records:
            self.tree_registrations.insert("", tk.END, values=record)

    def search_all_records(self):
        query = self.all_records_search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search query.")
            return

        for row in self.tree_all_records.get_children():
            self.tree_all_records.delete(row)

        self.database.cursor.execute(
            """
            SELECT 
                s.student_id, s.name, 
                c.course_id, c.course_name,
                i.instructor_id, i.name
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            WHERE 
                LOWER(s.student_id) LIKE ? OR 
                LOWER(s.name) LIKE ? OR
                LOWER(c.course_id) LIKE ? OR
                LOWER(c.course_name) LIKE ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
        )
        records = self.database.cursor.fetchall()
        for record in records:
            self.tree_all_records.insert("", tk.END, values=record)

    def reset_all_records_search(self):
        self.all_records_search_var.set("")
        self.populate_all_records()

    def search_students(self):
        query = self.students_search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search query.")
            return

        for row in self.tree_students.get_children():
            self.tree_students.delete(row)

        self.database.cursor.execute(
            """
            SELECT * FROM students
            WHERE 
                LOWER(student_id) LIKE ? OR 
                LOWER(name) LIKE ?
            """,
            (f"%{query}%", f"%{query}%")
        )
        students = self.database.cursor.fetchall()
        for student in students:
            self.tree_students.insert("", tk.END, values=student)

    def reset_students_search(self):
        self.students_search_var.set("")
        self.populate_students()

    def search_instructors(self):
        query = self.instructors_search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search query.")
            return

        for row in self.tree_instructors.get_children():
            self.tree_instructors.delete(row)

        self.database.cursor.execute(
            """
            SELECT * FROM instructors
            WHERE 
                LOWER(instructor_id) LIKE ? OR 
                LOWER(name) LIKE ?
            """,
            (f"%{query}%", f"%{query}%")
        )
        instructors = self.database.cursor.fetchall()
        for instructor in instructors:
            self.tree_instructors.insert("", tk.END, values=instructor)

    def reset_instructors_search(self):
        self.instructors_search_var.set("")
        self.populate_instructors()

    def search_courses(self):
        query = self.courses_search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search query.")
            return

        for row in self.tree_courses.get_children():
            self.tree_courses.delete(row)

        self.database.cursor.execute(
            """
            SELECT 
                c.course_id, c.course_name, c.instructor_id, i.name
            FROM courses c
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            WHERE 
                LOWER(c.course_id) LIKE ? OR 
                LOWER(c.course_name) LIKE ?
            """,
            (f"%{query}%", f"%{query}%")
        )
        courses = self.database.cursor.fetchall()
        for course in courses:
            instructor_name = course[3] if course[3] else "N/A"
            self.tree_courses.insert("", tk.END, values=(course[0], course[1], course[2] if course[2] else "N/A", instructor_name))

    def reset_courses_search(self):
        self.courses_search_var.set("")
        self.populate_courses()

    def search_registrations(self):
        query = self.registrations_search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search query.")
            return

        for row in self.tree_registrations.get_children():
            self.tree_registrations.delete(row)

        self.database.cursor.execute(
            """
            SELECT 
                r.id, s.student_id, s.name, c.course_id, c.course_name
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            WHERE 
                LOWER(s.student_id) LIKE ? OR 
                LOWER(s.name) LIKE ? OR
                LOWER(c.course_id) LIKE ? OR
                LOWER(c.course_name) LIKE ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
        )
        records = self.database.cursor.fetchall()
        for record in records:
            self.tree_registrations.insert("", tk.END, values=record)

    def reset_registrations_search(self):
        self.registrations_search_var.set("")
        self.populate_registrations()

    def save_data(self):
        filetypes = [("JSON files", "*.json"), ("CSV files", "*.csv")]
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=filetypes
        )
        if not filepath:
            return

        data = {
            "students": [{"student_id": s[0], "name": s[1], "age": s[2], "email": s[3]} for s in self.database.get_students()],
            "instructors": [{"instructor_id": i[0], "name": i[1], "age": i[2], "email": i[3]} for i in self.database.get_instructors()],
            "courses": [{"course_id": c[0], "course_name": c[1], "instructor_id": c[2]} for c in self.database.get_courses()],
            "registrations": [{"id": r[0], "student_id": r[1], "course_id": r[2]} for r in self.database.cursor.execute("SELECT * FROM registrations").fetchall()],
        }

        try:
            DataManagement.save_data(data, filepath)
            messagebox.showinfo("Success", f"Data saved successfully to {filepath}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_data(self):
        filetypes = [("JSON files", "*.json"), ("CSV files", "*.csv")]
        filepath = filedialog.askopenfilename(
            filetypes=filetypes
        )
        if not filepath:
            return

        try:
            data = DataManagement.load_data(filepath)
            if not isinstance(data, dict):
                messagebox.showerror("Error", "Invalid data format.")
                return

            self.clear_database()

            for s in data.get("students", []):
                student = Student(name=s["name"], age=int(s["age"]), _email=s["email"], student_id=s["student_id"])
                self.database.add_student(student)

            for i in data.get("instructors", []):
                instructor = Instructor(name=i["name"], age=int(i["age"]), _email=i["email"], instructor_id=i["instructor_id"])
                self.database.add_instructor(instructor)

            for c in data.get("courses", []):
                instructor = None
                if c["instructor_id"] != "None" and c["instructor_id"]:
                    instructor_record = self.database.get_instructor_by_id(c["instructor_id"])
                    if instructor_record:
                        instructor = Instructor(name=instructor_record[1], age=instructor_record[2], _email=instructor_record[3], instructor_id=instructor_record[0])
                course = Course(course_id=c["course_id"], course_name=c["course_name"], instructor=instructor)
                self.database.add_course(course)

            for r in data.get("registrations", []):
                self.database.register_student_to_course(r["student_id"], r["course_id"])

            self.populate_all_records()
            self.populate_students()
            self.populate_instructors()
            self.populate_courses()
            self.populate_registrations()

            messagebox.showinfo("Success", f"Data loaded successfully from {filepath}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def clear_database(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all existing data?")
        if not confirm:
            return

        try:
            self.database.cursor.execute("DELETE FROM registrations")
            self.database.cursor.execute("DELETE FROM courses")
            self.database.cursor.execute("DELETE FROM instructors")
            self.database.cursor.execute("DELETE FROM students")
            self.database.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear database: {e}")

    def attach_context_menu(self, treeview, tab_type):
        context_menu = Menu(self.master, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.edit_record(treeview, tab_type))
        context_menu.add_command(label="Delete", command=lambda: self.delete_record(treeview, tab_type))

        def show_context_menu(event):
            try:
                treeview.selection_set(treeview.identify_row(event.y))
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

        treeview.bind("<Button-3>", show_context_menu)

    def edit_record(self, treeview, tab_type):
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No record selected.")
            return

        values = treeview.item(selected_item, 'values')

        if tab_type == 'students':
            EditStudent(self.database, values, self.populate_students, self.populate_all_records)
        elif tab_type == 'instructors':
            EditInstructor(self.database, values, self.populate_instructors, self.populate_courses, self.populate_all_records)
        elif tab_type == 'courses':
            EditCourse(self.database, values, self.populate_courses, self.populate_all_records)
        elif tab_type == 'registrations':
            messagebox.showinfo("Info", "Registrations cannot be edited directly.")
        elif tab_type == 'all_records':
            messagebox.showinfo("Info", "Please use the specific tabs to edit records.")

    def delete_record(self, treeview, tab_type):
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No record selected.")
            return

        values = treeview.item(selected_item, 'values')

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record?")
        if not confirm:
            return

        try:
            if tab_type == 'students':
                student_id = values[0]
                self.database.delete_student(student_id)
                messagebox.showinfo("Success", f"Student ID {student_id} deleted successfully.")
                self.populate_students()
                self.populate_all_records()
            elif tab_type == 'instructors':
                instructor_id = values[0]
                self.database.delete_instructor(instructor_id)
                messagebox.showinfo("Success", f"Instructor ID {instructor_id} deleted successfully.")
                self.populate_instructors()
                self.populate_courses()
                self.populate_all_records()
            elif tab_type == 'courses':
                course_id = values[0]
                self.database.delete_course(course_id)
                messagebox.showinfo("Success", f"Course ID {course_id} deleted successfully.")
                self.populate_courses()
                self.populate_all_records()
            elif tab_type == 'registrations':
                registration_id = values[0]
                self.database.cursor.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
                self.database.conn.commit()
                messagebox.showinfo("Success", f"Registration ID {registration_id} deleted successfully.")
                self.populate_registrations()
                self.populate_all_records()
            elif tab_type == 'all_records':
                messagebox.showinfo("Info", "Please use the specific tabs to delete records.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")

    def new_student_window(self):
        AddStudent(self.database, self.populate_students, self.populate_all_records)

    def new_instructor_window(self):
        AddInstructor(self.database, self.populate_instructors, self.populate_courses, self.populate_all_records)

    def new_course_window(self):
        AddCourse(self.database, self.populate_courses, self.populate_all_records)

    def register_course_window(self):
        RegisterCourse(self.database, self.populate_registrations, self.populate_all_records)

    def assign_instructor_window(self):
        AssignInstructor(self.database, self.populate_courses, self.populate_all_records)


class AddStudent(Toplevel):
    def __init__(self, database, refresh_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Add a Student")
        self.database = database
        self.refresh_callback = refresh_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack(pady=(10, 0))
        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.pack(pady=5)

        self.label_age = tk.Label(self, text="Age:")
        self.label_age.pack(pady=(10, 0))
        self.entry_age = tk.Entry(self, width=50)
        self.entry_age.pack(pady=5)

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=(10, 0))
        self.entry_email = tk.Entry(self, width=50)
        self.entry_email.pack(pady=5)

        self.label_student_id = tk.Label(self, text="Student ID:")
        self.label_student_id.pack(pady=(10, 0))
        self.entry_student_id = tk.Entry(self, width=50)
        self.entry_student_id.pack(pady=5)

        self.button_add = Button(
            self, text="Add Student", width=25, command=self.add_student
        )
        self.button_add.pack(pady=20)

    def add_student(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        email = self.entry_email.get().strip()
        student_id = self.entry_student_id.get().strip()

        if not name or not age or not email or not student_id:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be an integer.")
            return

        try:
            new_student = Student(name, age, email, student_id)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error creating student: {e}")
            return

        success = self.database.add_student(new_student)
        if success:
            messagebox.showinfo(
                "Success", f"Student {new_student.name} added to the database!"
            )
            self.refresh_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to add student. Please check the details."
            )


class AddInstructor(Toplevel):
    def __init__(self, database, refresh_callback, refresh_courses_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Add an Instructor")
        self.database = database
        self.refresh_callback = refresh_callback
        self.refresh_courses_callback = refresh_courses_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack(pady=(10, 0))
        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.pack(pady=5)

        self.label_age = tk.Label(self, text="Age:")
        self.label_age.pack(pady=(10, 0))
        self.entry_age = tk.Entry(self, width=50)
        self.entry_age.pack(pady=5)

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=(10, 0))
        self.entry_email = tk.Entry(self, width=50)
        self.entry_email.pack(pady=5)

        self.label_instructor_id = tk.Label(self, text="Instructor ID:")
        self.label_instructor_id.pack(pady=(10, 0))
        self.entry_instructor_id = tk.Entry(self, width=50)
        self.entry_instructor_id.pack(pady=5)

        self.button_add = Button(
            self, text="Add Instructor", width=25, command=self.add_instructor
        )
        self.button_add.pack(pady=20)

    def add_instructor(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        email = self.entry_email.get().strip()
        instructor_id = self.entry_instructor_id.get().strip()

        if not name or not age or not email or not instructor_id:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be an integer.")
            return

        try:
            new_instructor = Instructor(name, age, email, instructor_id)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error creating instructor: {e}")
            return

        success = self.database.add_instructor(new_instructor)
        if success:
            messagebox.showinfo(
                "Success", f"Instructor {new_instructor.name} added to the database!"
            )
            self.refresh_callback()
            self.refresh_courses_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to add instructor. Please check the details."
            )


class AddCourse(Toplevel):
    def __init__(self, database, refresh_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Add a Course")
        self.database = database
        self.refresh_callback = refresh_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.label_course_id = tk.Label(self, text="Course ID:")
        self.label_course_id.pack(pady=(10, 0))
        self.entry_course_id = tk.Entry(self, width=50)
        self.entry_course_id.pack(pady=5)

        self.label_course_name = tk.Label(self, text="Course Name:")
        self.label_course_name.pack(pady=(10, 0))
        self.entry_course_name = tk.Entry(self, width=50)
        self.entry_course_name.pack(pady=5)

        self.label_instructor = tk.Label(self, text="Assign Instructor (Optional):")
        self.label_instructor.pack(pady=(10, 0))

        instructors = self.database.get_instructors()
        instructor_list = [f"{instr[0]}: {instr[1]}" for instr in instructors]
        instructor_list.insert(0, "None")

        self.selected_instructor = tk.StringVar(self)
        self.selected_instructor.set(instructor_list[0])
        self.dropdown_instructors = ttk.Combobox(
            self,
            textvariable=self.selected_instructor,
            values=instructor_list,
            state="readonly",
            width=47,
        )
        self.dropdown_instructors.pack(pady=5)

        self.button_add = Button(
            self, text="Add Course", width=25, command=self.add_course
        )
        self.button_add.pack(pady=20)

    def add_course(self):
        course_id = self.entry_course_id.get().strip()
        course_name = self.entry_course_name.get().strip()
        selected_instructor = self.selected_instructor.get()

        if not course_id or not course_name:
            messagebox.showerror(
                "Input Error", "Course ID and Course Name are required!"
            )
            return

        if selected_instructor == "None":
            instructor = None
        else:
            try:
                instructor_id, instructor_name = selected_instructor.split(": ", 1)
                instructor_record = self.database.get_instructor_by_id(instructor_id)
                if not instructor_record:
                    messagebox.showerror("Error", "Selected instructor does not exist.")
                    return
                instructor = Instructor(
                    name=instructor_record[1],
                    age=instructor_record[2],
                    _email=instructor_record[3],
                    instructor_id=instructor_record[0],
                )
            except ValueError:
                messagebox.showerror("Input Error", "Invalid instructor selection.")
                return

        try:
            new_course = Course(course_id, course_name, instructor)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error creating course: {e}")
            return

        success = self.database.add_course(new_course)
        if success:
            messagebox.showinfo(
                "Success", f"Course {new_course.course_name} added to the database!"
            )
            self.refresh_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to add course. Please check the details."
            )


class RegisterCourse(Toplevel):
    def __init__(self, database, refresh_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Register Student for a Course")
        self.database = database
        self.refresh_callback = refresh_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.label_student = tk.Label(self, text="Select Student:")
        self.label_student.pack(pady=(10, 0))

        self.student_options = self.get_students()
        if not self.student_options:
            messagebox.showerror("No Students", "No students available to register.")
            self.destroy()
            return

        self.selected_student = tk.StringVar(self)
        self.selected_student.set(self.student_options[0])

        self.dropdown_students = ttk.Combobox(
            self,
            textvariable=self.selected_student,
            values=self.student_options,
            state="readonly",
            width=47,
        )
        self.dropdown_students.pack(pady=5)

        self.label_course = tk.Label(self, text="Select Course:")
        self.label_course.pack(pady=(10, 0))

        self.course_options = self.get_courses()
        if not self.course_options:
            messagebox.showerror("No Courses", "No courses available to register.")
            self.destroy()
            return

        self.selected_course = tk.StringVar(self)
        self.selected_course.set(self.course_options[0])

        self.dropdown_courses = ttk.Combobox(
            self,
            textvariable=self.selected_course,
            values=self.course_options,
            state="readonly",
            width=47,
        )
        self.dropdown_courses.pack(pady=5)

        self.button_register = Button(
            self, text="Register", width=25, command=self.register
        )
        self.button_register.pack(pady=20)

    def get_students(self) -> list[str]:
        students = self.database.get_students()
        return [f"{student[0]}: {student[1]}" for student in students]

    def get_courses(self) -> list[str]:
        courses = self.database.get_courses()
        return [f"{course[0]}: {course[1]}" for course in courses]

    def register(self):
        selected_student = self.selected_student.get()
        selected_course = self.selected_course.get()

        if not selected_student or not selected_course:
            messagebox.showerror(
                "Input Error", "Both Student and Course must be selected!"
            )
            return

        try:
            student_id, student_name = selected_student.split(": ", 1)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid student selection.")
            return

        try:
            course_id, course_name = selected_course.split(": ", 1)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid course selection.")
            return

        student_record = self.database.get_student_by_id(student_id)
        if not student_record:
            messagebox.showerror("Error", f"Student ID {student_id} does not exist.")
            return

        success = self.database.register_student_to_course(student_id, course_id)
        if success:
            messagebox.showinfo(
                "Success", f"Student {student_record[1]} registered for {course_name}!"
            )
            self.refresh_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to register student for the course.")


class AssignInstructor(Toplevel):
    def __init__(self, database, refresh_courses_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Assign Instructor to Course")
        self.database = database
        self.refresh_courses_callback = refresh_courses_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.label_instructor = tk.Label(self, text="Select Instructor:")
        self.label_instructor.pack(pady=(10, 0))

        self.instructor_options = self.get_instructors()
        if not self.instructor_options:
            messagebox.showerror(
                "No Instructors", "No instructors available to assign."
            )
            self.destroy()
            return

        self.selected_instructor = tk.StringVar(self)
        self.selected_instructor.set(self.instructor_options[0])

        self.dropdown_instructors = ttk.Combobox(
            self,
            textvariable=self.selected_instructor,
            values=self.instructor_options,
            state="readonly",
            width=47,
        )
        self.dropdown_instructors.pack(pady=5)

        self.label_course = tk.Label(self, text="Select Course:")
        self.label_course.pack(pady=(10, 0))

        self.course_options = self.get_courses()
        if not self.course_options:
            messagebox.showerror(
                "No Courses", "No courses available to assign instructors."
            )
            self.destroy()
            return

        self.selected_course = tk.StringVar(self)
        self.selected_course.set(self.course_options[0])

        self.dropdown_courses = ttk.Combobox(
            self,
            textvariable=self.selected_course,
            values=self.course_options,
            state="readonly",
            width=47,
        )
        self.dropdown_courses.pack(pady=5)

        self.button_assign = Button(
            self, text="Assign Instructor", width=25, command=self.assign
        )
        self.button_assign.pack(pady=20)

    def get_instructors(self) -> list[str]:
        instructors = self.database.get_instructors()
        return [f"{instr[0]}: {instr[1]}" for instr in instructors]

    def get_courses(self) -> list[str]:
        courses = self.database.get_courses()
        return [f"{course[0]}: {course[1]}" for course in courses]

    def assign(self):
        selected_instructor = self.selected_instructor.get()
        selected_course = self.selected_course.get()

        if not selected_instructor or not selected_course:
            messagebox.showerror(
                "Input Error", "Both Instructor and Course must be selected!"
            )
            return

        try:
            instructor_id, instructor_name = selected_instructor.split(": ", 1)
            course_id, course_name = selected_course.split(": ", 1)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid selection format.")
            return

        success = self.database.assign_instructor_to_course(instructor_id, course_id)
        if success:
            messagebox.showinfo(
                "Success", f"Instructor {instructor_name} assigned to {course_name}!"
            )
            self.refresh_courses_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to assign instructor to the course.")


class EditStudent(Toplevel):
    def __init__(self, database, student_values, refresh_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Edit Student")
        self.database = database
        self.student_id = student_values[0]
        self.refresh_callback = refresh_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.student_record = self.database.get_student_by_id(self.student_id)
        if not self.student_record:
            messagebox.showerror("Error", "Selected student does not exist.")
            self.destroy()
            return

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack(pady=(10, 0))
        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.insert(0, self.student_record[1])
        self.entry_name.pack(pady=5)

        self.label_age = tk.Label(self, text="Age:")
        self.label_age.pack(pady=(10, 0))
        self.entry_age = tk.Entry(self, width=50)
        self.entry_age.insert(0, self.student_record[2])
        self.entry_age.pack(pady=5)

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=(10, 0))
        self.entry_email = tk.Entry(self, width=50)
        self.entry_email.insert(0, self.student_record[3])
        self.entry_email.pack(pady=5)

        self.button_update = Button(
            self, text="Update Student", width=25, command=self.update_student
        )
        self.button_update.pack(pady=20)

    def update_student(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        email = self.entry_email.get().strip()

        if not name or not age or not email:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be an integer.")
            return

        try:
            updated_student = Student(name, age, email, self.student_id)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error updating student: {e}")
            return

        success = self.database.update_student(updated_student)
        if success:
            messagebox.showinfo(
                "Success", f"Student {updated_student.name} updated successfully!"
            )
            self.refresh_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to update student. Please check the details."
            )


class EditInstructor(Toplevel):
    def __init__(self, database, instructor_values, refresh_callback, refresh_courses_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Edit Instructor")
        self.database = database
        self.instructor_id = instructor_values[0]
        self.refresh_callback = refresh_callback
        self.refresh_courses_callback = refresh_courses_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.instructor_record = self.database.get_instructor_by_id(self.instructor_id)
        if not self.instructor_record:
            messagebox.showerror("Error", "Selected instructor does not exist.")
            self.destroy()
            return

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack(pady=(10, 0))
        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.insert(0, self.instructor_record[1])
        self.entry_name.pack(pady=5)

        self.label_age = tk.Label(self, text="Age:")
        self.label_age.pack(pady=(10, 0))
        self.entry_age = tk.Entry(self, width=50)
        self.entry_age.insert(0, self.instructor_record[2])
        self.entry_age.pack(pady=5)

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=(10, 0))
        self.entry_email = tk.Entry(self, width=50)
        self.entry_email.insert(0, self.instructor_record[3])
        self.entry_email.pack(pady=5)

        self.button_update = Button(
            self, text="Update Instructor", width=25, command=self.update_instructor
        )
        self.button_update.pack(pady=20)

    def update_instructor(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        email = self.entry_email.get().strip()

        if not name or not age or not email:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be an integer.")
            return

        try:
            updated_instructor = Instructor(name, age, email, self.instructor_id)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error updating instructor: {e}")
            return

        success = self.database.update_instructor(updated_instructor)
        if success:
            messagebox.showinfo(
                "Success", f"Instructor {updated_instructor.name} updated successfully!"
            )
            self.refresh_callback()
            self.refresh_courses_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to update instructor. Please check the details."
            )


class EditCourse(Toplevel):
    def __init__(self, database, course_values, refresh_callback, refresh_all_records_callback):
        super().__init__()
        self.title("Edit Course")
        self.database = database
        self.course_id = course_values[0]
        self.refresh_callback = refresh_callback
        self.refresh_all_records_callback = refresh_all_records_callback

        self.course_record = self.database.get_course_by_id(self.course_id)
        if not self.course_record:
            messagebox.showerror("Error", "Selected course does not exist.")
            self.destroy()
            return

        self.label_course_name = tk.Label(self, text="Course Name:")
        self.label_course_name.pack(pady=(10, 0))
        self.entry_course_name = tk.Entry(self, width=50)
        self.entry_course_name.insert(0, self.course_record[1])
        self.entry_course_name.pack(pady=5)

        self.label_instructor = tk.Label(self, text="Assign Instructor (Optional):")
        self.label_instructor.pack(pady=(10, 0))

        instructors = self.database.get_instructors()
        instructor_list = [f"{instr[0]}: {instr[1]}" for instr in instructors]
        instructor_list.insert(0, "None")

        self.selected_instructor = tk.StringVar(self)
        current_instructor_id = self.course_record[2] if self.course_record[2] else "None"
        if current_instructor_id != "None" and current_instructor_id:
            instructor_name = next((f"{instr[0]}: {instr[1]}" for instr in instructors if instr[0] == current_instructor_id), "None")
            self.selected_instructor.set(instructor_name)
        else:
            self.selected_instructor.set("None")

        self.dropdown_instructors = ttk.Combobox(
            self,
            textvariable=self.selected_instructor,
            values=instructor_list,
            state="readonly",
            width=47,
        )
        self.dropdown_instructors.pack(pady=5)

        self.button_update = Button(
            self, text="Update Course", width=25, command=self.update_course
        )
        self.button_update.pack(pady=20)

    def update_course(self):
        course_name = self.entry_course_name.get().strip()
        selected_instructor = self.selected_instructor.get()

        if not course_name:
            messagebox.showerror(
                "Input Error", "Course Name is required!"
            )
            return

        if selected_instructor == "None":
            instructor = None
        else:
            try:
                instructor_id, instructor_name = selected_instructor.split(": ", 1)
                instructor_record = self.database.get_instructor_by_id(instructor_id)
                if not instructor_record:
                    messagebox.showerror("Error", "Selected instructor does not exist.")
                    return
                instructor = Instructor(
                    name=instructor_record[1],
                    age=instructor_record[2],
                    _email=instructor_record[3],
                    instructor_id=instructor_record[0],
                )
            except ValueError:
                messagebox.showerror("Input Error", "Invalid instructor selection.")
                return

        try:
            updated_course = Course(course_id=self.course_id, course_name=course_name, instructor=instructor)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Error updating course: {e}")
            return

        success = self.database.update_course(updated_course)
        if success:
            messagebox.showinfo(
                "Success", f"Course {updated_course.course_name} updated successfully!"
            )
            self.refresh_callback()
            self.refresh_all_records_callback()
            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Failed to update course. Please check the details."
            )


def main():
    root = tk.Tk()
    app = SchoolManagementSystem(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
