# pyqt_gui.py

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox

class SchoolManagementSystemPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('School Management System - PyQt5')

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Student form
        self.student_name_label = QLabel('Student Name:')
        layout.addWidget(self.student_name_label)
        self.student_name_entry = QLineEdit()
        layout.addWidget(self.student_name_entry)

        self.student_age_label = QLabel('Student Age:')
        layout.addWidget(self.student_age_label)
        self.student_age_entry = QLineEdit()
        layout.addWidget(self.student_age_entry)

        self.add_student_button = QPushButton('Add Student')
        layout.addWidget(self.add_student_button)
        self.add_student_button.clicked.connect(self.add_student)

        # Instructor form
        self.instructor_name_label = QLabel('Instructor Name:')
        layout.addWidget(self.instructor_name_label)
        self.instructor_name_entry = QLineEdit()
        layout.addWidget(self.instructor_name_entry)

        self.instructor_age_label = QLabel('Instructor Age:')
        layout.addWidget(self.instructor_age_label)
        self.instructor_age_entry = QLineEdit()
        layout.addWidget(self.instructor_age_entry)

        self.add_instructor_button = QPushButton('Add Instructor')
        layout.addWidget(self.add_instructor_button)
        self.add_instructor_button.clicked.connect(self.add_instructor)

    def add_student(self):
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        if name and age:
            QMessageBox.information(self, 'Success', f'Student {name} added successfully.')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')

    def add_instructor(self):
        name = self.instructor_name_entry.text()
        age = self.instructor_age_entry.text()
        if name and age:
            QMessageBox.information(self, 'Success', f'Instructor {name} added successfully.')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystemPyQt()
    window.show()
    sys.exit(app.exec_())
