import json
import re

# Class 1: Define the Person Class
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = self._validate_age(age)
        self._email = self._validate_email(email)  # Private email attribute

    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    # Private method to validate email
    def _validate_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email):
            return email
        else:
            raise ValueError(f"Invalid email format: {email}")

    # Private method to validate age
    def _validate_age(self, age):
        if age >= 0:
            return age
        else:
            raise ValueError(f"Age must be a non-negative integer: {age}")

# Class 2: Define the Student Subclass
class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)  # Inherits from Person
        self.student_id = student_id
        self.registered_courses = []  # List of Course objects

    # Method to register for a course
    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)
        else:
            print(f"Student {self.name} is already registered for {course.course_name}.")

    # Introduce method for Student
    def introduce(self):
        print(f"Hello, I am {self.name}, a student with ID {self.student_id}.")

# Class 3: Define the Instructor Subclass
class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)  # Inherits from Person
        self.instructor_id = instructor_id
        self.assigned_courses = []  # List of Course objects

    # Method to assign an instructor to a course
    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self  # Set the course's instructor
        else:
            print(f"Instructor {self.name} is already assigned to {course.course_name}.")

    # Introduce method for Instructor
    def introduce(self):
        print(f"Hello, I am {self.name}, an instructor with ID {self.instructor_id}.")

# Class 4: Define the Course Class
class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None  # Instructor assigned to the course
        self.enrolled_students = []  # List of Student objects

    # Method to add a student to a course
    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
        else:
            print(f"Student {student.name} is already enrolled in {self.course_name}.")

    # Display course details
    def course_details(self):
        instructor_name = self.instructor.name if self.instructor else "No instructor assigned"
        print(f"Course {self.course_name} (ID: {self.course_id}) is taught by {instructor_name}.")
        print(f"Enrolled students: {[student.name for student in self.enrolled_students]}")

# Data management: Serialization (Save and Load)
def save_data(students, instructors, courses, filename="school_data.json"):
    data = {
        "students": [
            {
                "name": student.name,
                "age": student.age,
                "email": student._email,
                "student_id": student.student_id,
                "registered_courses": [course.course_id for course in student.registered_courses]
            } for student in students
        ],
        "instructors": [
            {
                "name": instructor.name,
                "age": instructor.age,
                "email": instructor._email,
                "instructor_id": instructor.instructor_id,
                "assigned_courses": [course.course_id for course in instructor.assigned_courses]
            } for instructor in instructors
        ],
        "courses": [
            {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "instructor": course.instructor.instructor_id if course.instructor else None,
                "enrolled_students": [student.student_id for student in course.enrolled_students]
            } for course in courses
        ]
    }
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def load_data(filename="school_data.json"):
    with open(filename, 'r') as file:
        data = json.load(file)

    students = []
    instructors = []
    courses = []

    # Create Course objects first (we need them for students and instructors)
    course_dict = {}
    for course_data in data['courses']:
        course = Course(course_data['course_id'], course_data['course_name'])
        courses.append(course)
        course_dict[course.course_id] = course

    # Create Student objects
    for student_data in data['students']:
        student = Student(
            name=student_data['name'], 
            age=student_data['age'], 
            email=student_data['email'], 
            student_id=student_data['student_id']
        )
        # Register courses for student
        for course_id in student_data['registered_courses']:
            course = course_dict[course_id]
            student.register_course(course)
        students.append(student)

    # Create Instructor objects
    for instructor_data in data['instructors']:
        instructor = Instructor(
            name=instructor_data['name'], 
            age=instructor_data['age'], 
            email=instructor_data['email'], 
            instructor_id=instructor_data['instructor_id']
        )
        # Assign courses to instructor
        for course_id in instructor_data['assigned_courses']:
            course = course_dict[course_id]
            instructor.assign_course(course)
        instructors.append(instructor)

    return students, instructors, courses
