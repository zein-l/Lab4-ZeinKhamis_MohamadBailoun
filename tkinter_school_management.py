import tkinter as tk
from tkinter import ttk, messagebox
from oop_school_management import Student, Instructor, Course, save_data, load_data

class SchoolManagementSystemTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("800x600")

        # Data storage for students, instructors, and courses
        self.students = []
        self.instructors = []
        self.courses = []

        # Create the forms and buttons
        self.create_forms()

        # Load data if available
        self.load_existing_data()

    def create_forms(self):
        # Create Tabs
        tab_control = ttk.Notebook(self)
        student_tab = ttk.Frame(tab_control)
        instructor_tab = ttk.Frame(tab_control)
        course_tab = ttk.Frame(tab_control)
        tab_control.add(student_tab, text="Students")
        tab_control.add(instructor_tab, text="Instructors")
        tab_control.add(course_tab, text="Courses")
        tab_control.pack(expand=1, fill="both")

        # Student form
        self.student_name = tk.Entry(student_tab)
        self.student_id = tk.Entry(student_tab)
        self.create_form(student_tab, "Student Name", self.student_name, "Student ID", self.student_id, self.add_student)

        # Instructor form
        self.instructor_name = tk.Entry(instructor_tab)
        self.instructor_id = tk.Entry(instructor_tab)
        self.create_form(instructor_tab, "Instructor Name", self.instructor_name, "Instructor ID", self.instructor_id, self.add_instructor)

        # Course form
        self.course_name = tk.Entry(course_tab)
        self.course_id = tk.Entry(course_tab)
        self.create_form(course_tab, "Course Name", self.course_name, "Course ID", self.course_id, self.add_course)

        # Registration Form for Students
        self.create_registration_form()

        # Display Table (Treeview)
        self.create_display_table()

    def create_form(self, parent, label1_text, entry1, label2_text, entry2, add_func):
        tk.Label(parent, text=label1_text).grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        tk.Label(parent, text=label2_text).grid(row=1, column=0)
        entry2.grid(row=1, column=1)
        add_btn = tk.Button(parent, text="Add", command=add_func)
        add_btn.grid(row=2, column=1)

    def create_registration_form(self):
        # Dropdown for registering students to courses
        self.registration_frame = ttk.LabelFrame(self, text="Student Course Registration")
        self.registration_frame.pack(fill="both", padx=20, pady=10)
        
        tk.Label(self.registration_frame, text="Select Student:").grid(row=0, column=0)
        self.student_dropdown = ttk.Combobox(self.registration_frame)
        self.student_dropdown.grid(row=0, column=1)

        tk.Label(self.registration_frame, text="Select Course:").grid(row=1, column=0)
        self.course_dropdown = ttk.Combobox(self.registration_frame)
        self.course_dropdown.grid(row=1, column=1)

        register_btn = tk.Button(self.registration_frame, text="Register Student", command=self.register_student)
        register_btn.grid(row=2, column=1)

    def create_display_table(self):
        self.table_frame = ttk.LabelFrame(self, text="All Records")
        self.table_frame.pack(fill="both", padx=20, pady=10)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.table_frame, columns=("type", "name", "id", "extra"), show="headings")
        self.tree.heading("type", text="Type")
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="ID")
        self.tree.heading("extra", text="Additional Info")
        self.tree.pack(fill="both", expand=True)

        # Add refresh button to refresh the table
        refresh_btn = tk.Button(self.table_frame, text="Refresh", command=self.refresh_table)
        refresh_btn.pack(pady=10)

    # Function to add a student
    def add_student(self):
        name = self.student_name.get()
        student_id = self.student_id.get()
        if name and student_id:
            student = Student(name, 20, "example@example.com", student_id)
            self.students.append(student)
            self.student_dropdown['values'] = [student.name for student in self.students]
            messagebox.showinfo("Success", f"Student {name} added.")
        else:
            messagebox.showerror("Error", "Please enter all fields.")

    # Function to add an instructor
    def add_instructor(self):
        name = self.instructor_name.get()
        instructor_id = self.instructor_id.get()
        if name and instructor_id:
            instructor = Instructor(name, 30, "instructor@example.com", instructor_id)
            self.instructors.append(instructor)
            messagebox.showinfo("Success", f"Instructor {name} added.")
        else:
            messagebox.showerror("Error", "Please enter all fields.")

    # Function to add a course
    def add_course(self):
        name = self.course_name.get()
        course_id = self.course_id.get()
        if name and course_id:
            course = Course(course_id, name)
            self.courses.append(course)
            self.course_dropdown['values'] = [course.course_name for course in self.courses]
            messagebox.showinfo("Success", f"Course {name} added.")
        else:
            messagebox.showerror("Error", "Please enter all fields.")

    # Function to register a student for a course
    def register_student(self):
        selected_student_name = self.student_dropdown.get()
        selected_course_name = self.course_dropdown.get()
        student = next((s for s in self.students if s.name == selected_student_name), None)
        course = next((c for c in self.courses if c.course_name == selected_course_name), None)
        if student and course:
            student.register_course(course)
            messagebox.showinfo("Success", f"Student {student.name} registered for {course.course_name}")
        else:
            messagebox.showerror("Error", "Please select valid student and course.")

    # Function to refresh the display table
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.students:
            self.tree.insert("", "end", values=("Student", student.name, student.student_id, f"Courses: {[course.course_name for course in student.registered_courses]}"))
        for instructor in self.instructors:
            self.tree.insert("", "end", values=("Instructor", instructor.name, instructor.instructor_id, f"Courses: {[course.course_name for course in instructor.assigned_courses]}"))
        for course in self.courses:
            self.tree.insert("", "end", values=("Course", course.course_name, course.course_id, f"Instructor: {course.instructor.name if course.instructor else 'None'}"))

    # Function to load existing data from a file
    def load_existing_data(self):
        try:
            self.students, self.instructors, self.courses = load_data()
            messagebox.showinfo("Success", "Data loaded successfully.")
            self.refresh_table()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved data found.")

    # Function to save data to a file
    def save_data(self):
        save_data(self.students, self.instructors, self.courses)
        messagebox.showinfo("Success", "Data saved successfully.")

if __name__ == "__main__":
    app = SchoolManagementSystemTk()
    app.mainloop()
