# tkinter_gui.py

import tkinter as tk
from tkinter import messagebox

class SchoolManagementSystemTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System - Tkinter")

        # Student form
        self.student_name_label = tk.Label(root, text="Student Name")
        self.student_name_label.pack()
        self.student_name_entry = tk.Entry(root)
        self.student_name_entry.pack()

        self.student_age_label = tk.Label(root, text="Student Age")
        self.student_age_label.pack()
        self.student_age_entry = tk.Entry(root)
        self.student_age_entry.pack()

        self.add_student_button = tk.Button(root, text="Add Student", command=self.add_student)
        self.add_student_button.pack()

        # Instructor form
        self.instructor_name_label = tk.Label(root, text="Instructor Name")
        self.instructor_name_label.pack()
        self.instructor_name_entry = tk.Entry(root)
        self.instructor_name_entry.pack()

        self.instructor_age_label = tk.Label(root, text="Instructor Age")
        self.instructor_age_label.pack()
        self.instructor_age_entry = tk.Entry(root)
        self.instructor_age_entry.pack()

        self.add_instructor_button = tk.Button(root, text="Add Instructor", command=self.add_instructor)
        self.add_instructor_button.pack()

    def add_student(self):
        name = self.student_name_entry.get()
        age = self.student_age_entry.get()
        if name and age:
            messagebox.showinfo("Success", f"Student {name} added successfully.")
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

    def add_instructor(self):
        name = self.instructor_name_entry.get()
        age = self.instructor_age_entry.get()
        if name and age:
            messagebox.showinfo("Success", f"Instructor {name} added successfully.")
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SchoolManagementSystemTkinter(root)
    root.mainloop()
