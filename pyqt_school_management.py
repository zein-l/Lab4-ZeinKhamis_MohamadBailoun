import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QComboBox, QHBoxLayout
)
from oop_school_management import Student, Instructor, Course


class SchoolManagementSystemQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1000, 600)

        # Data storage (in memory for now)
        self.students = []
        self.instructors = []
        self.courses = []

        # Main layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Student, Instructor, and Course forms
        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.instructor_tab, "Instructors")
        self.tabs.addTab(self.course_tab, "Courses")

        # Create forms and table
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_table()

    def create_student_form(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()

        # Student Name and ID Input
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText("Enter Student Name")
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Enter Student ID")

        form_layout.addWidget(QLabel("Student Name:"))
        form_layout.addWidget(self.student_name_input)
        form_layout.addWidget(QLabel("Student ID:"))
        form_layout.addWidget(self.student_id_input)

        # Add Student Button
        self.add_student_btn = QPushButton("Add Student")
        self.add_student_btn.clicked.connect(self.add_student)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_student_btn)

        # Assign student to course layout
        assign_layout = QHBoxLayout()

        self.student_dropdown = QComboBox()
        self.course_dropdown_student = QComboBox()  # This is for the course selection in the student form

        self.assign_student_btn = QPushButton("Assign Student to Course")
        self.assign_student_btn.clicked.connect(self.assign_student_to_course)

        assign_layout.addWidget(QLabel("Select Student:"))
        assign_layout.addWidget(self.student_dropdown)
        assign_layout.addWidget(QLabel("Select Course:"))
        assign_layout.addWidget(self.course_dropdown_student)  # Adding course dropdown for student
        assign_layout.addWidget(self.assign_student_btn)

        layout.addLayout(assign_layout)

        self.student_tab.setLayout(layout)

    def create_instructor_form(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()

        # Instructor Name and ID Input
        self.instructor_name_input = QLineEdit()
        self.instructor_name_input.setPlaceholderText("Enter Instructor Name")
        self.instructor_id_input = QLineEdit()
        self.instructor_id_input.setPlaceholderText("Enter Instructor ID")

        form_layout.addWidget(QLabel("Instructor Name:"))
        form_layout.addWidget(self.instructor_name_input)
        form_layout.addWidget(QLabel("Instructor ID:"))
        form_layout.addWidget(self.instructor_id_input)

        # Add Instructor Button
        self.add_instructor_btn = QPushButton("Add Instructor")
        self.add_instructor_btn.clicked.connect(self.add_instructor)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_instructor_btn)

        # Assign instructor to course layout
        self.instructor_dropdown = QComboBox()
        self.course_dropdown_instructor = QComboBox()  # Adding course dropdown for instructor

        self.assign_instructor_btn = QPushButton("Assign Instructor to Course")
        self.assign_instructor_btn.clicked.connect(self.assign_instructor_to_course)

        assign_layout = QHBoxLayout()
        assign_layout.addWidget(QLabel("Select Instructor:"))
        assign_layout.addWidget(self.instructor_dropdown)
        assign_layout.addWidget(QLabel("Select Course:"))
        assign_layout.addWidget(self.course_dropdown_instructor)  # Adding course dropdown for instructor
        assign_layout.addWidget(self.assign_instructor_btn)

        layout.addLayout(assign_layout)

        self.instructor_tab.setLayout(layout)

    def create_course_form(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()

        # Course Name and ID Input
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Enter Course Name")
        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText("Enter Course ID")

        form_layout.addWidget(QLabel("Course Name:"))
        form_layout.addWidget(self.course_name_input)
        form_layout.addWidget(QLabel("Course ID:"))
        form_layout.addWidget(self.course_id_input)

        # Add Course Button
        self.add_course_btn = QPushButton("Add Course")
        self.add_course_btn.clicked.connect(self.add_course)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_course_btn)

        self.course_tab.setLayout(layout)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Type", "Name", "ID", "Additional Info"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make the table read-only
        self.tabs.addTab(self.table, "All Records")

        # Add refresh button styled as a button
        self.refresh_btn = QPushButton("Refresh Table")
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.tabs.addTab(self.refresh_btn, "Refresh Table")

    # Add Student
    def add_student(self):
        name = self.student_name_input.text()
        student_id = self.student_id_input.text()
        if name and student_id:
            student = Student(name, 20, "student@example.com", student_id)
            self.students.append(student)
            self.student_dropdown.addItem(student.name)
            QMessageBox.information(self, "Success", f"Student {name} added successfully.")
            self.student_name_input.clear()
            self.student_id_input.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")

    # Add Instructor
    def add_instructor(self):
        name = self.instructor_name_input.text()
        instructor_id = self.instructor_id_input.text()
        if name and instructor_id:
            instructor = Instructor(name, 30, "instructor@example.com", instructor_id)
            self.instructors.append(instructor)
            self.instructor_dropdown.addItem(instructor.name)
            QMessageBox.information(self, "Success", f"Instructor {name} added successfully.")
            self.instructor_name_input.clear()
            self.instructor_id_input.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")

    # Add Course
    def add_course(self):
        name = self.course_name_input.text()
        course_id = self.course_id_input.text()
        if name and course_id:
            course = Course(course_id, name)
            self.courses.append(course)
            self.course_dropdown_student.addItem(course.course_name)  # Add course to student section dropdown
            self.course_dropdown_instructor.addItem(course.course_name)  # Add course to instructor section dropdown
            QMessageBox.information(self, "Success", f"Course {name} added successfully.")
            self.course_name_input.clear()
            self.course_id_input.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")

    # Assign Student to Course
    def assign_student_to_course(self):
        student_name = self.student_dropdown.currentText()
        course_name = self.course_dropdown_student.currentText()
        student = next((s for s in self.students if s.name == student_name), None)
        course = next((c for c in self.courses if c.course_name == course_name), None)
        if student and course:
            student.register_course(course)
            QMessageBox.information(self, "Success", f"Student {student_name} assigned to {course_name}.")
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", "Invalid student or course selection.")

    # Assign Instructor to Course
    def assign_instructor_to_course(self):
        instructor_name = self.instructor_dropdown.currentText()
        course_name = self.course_dropdown_instructor.currentText()
        instructor = next((i for i in self.instructors if i.name == instructor_name), None)
        course = next((c for c in self.courses if c.course_name == course_name), None)
        if instructor and course:
            instructor.assign_course(course)
            QMessageBox.information(self, "Success", f"Instructor {instructor_name} assigned to {course_name}.")
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", "Invalid instructor or course selection.")

    # Refresh the table
    def refresh_table(self):
        # Step 1: Clear the table before inserting new rows
        self.table.setRowCount(0)

        # Step 2: Populate students
        for student in self.students:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Student"))
            self.table.setItem(row, 1, QTableWidgetItem(student.name))
            self.table.setItem(row, 2, QTableWidgetItem(student.student_id))
            self.table.setItem(row, 3, QTableWidgetItem(f"Courses: {[course.course_name for course in student.registered_courses]}"))

        # Step 3: Populate instructors
        for instructor in self.instructors:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Instructor"))
            self.table.setItem(row, 1, QTableWidgetItem(instructor.name))
            self.table.setItem(row, 2, QTableWidgetItem(instructor.instructor_id))
            self.table.setItem(row, 3, QTableWidgetItem(f"Courses: {[course.course_name for course in instructor.assigned_courses]}"))

        # Step 4: Populate courses
        for course in self.courses:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Course"))
            self.table.setItem(row, 1, QTableWidgetItem(course.course_name))
            self.table.setItem(row, 2, QTableWidgetItem(course.course_id))
            self.table.setItem(row, 3, QTableWidgetItem(f"Instructor: {course.instructor.name if course.instructor else 'None'}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystemQt()
    window.show()
    sys.exit(app.exec_())
