# oop.py

class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self._email = email  # private attribute

    def introduce(self):
        print(f"Hello, my name is {self.name}, and I am {self.age} years old.")

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        self.registered_courses.append(course)
        print(f"{self.name} has registered for {course.course_name}.")

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        self.assigned_courses.append(course)
        print(f"{self.name} has been assigned to teach {course.course_name}.")

class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        self.enrolled_students.append(student)
        print(f"{student.name} has been enrolled in {self.course_name}.")
