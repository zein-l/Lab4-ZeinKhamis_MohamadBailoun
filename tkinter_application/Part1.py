import csv
import json
import os
from email.utils import parseaddr


class Person:
    """
    A class used to represent a Person.

    Attributes:
    ----------
    name : str
        the name of the person
    age : int
        the age of the person, must be a non-negative integer
    email : str
        the email address of the person

    Methods:
    -------
    introduce():
        Prints a greeting with the person's name and age.
    validate_age(age: int):
        Validates the person's age, ensuring it is non-negative.
    validate_email(email: str):
        Validates the email format.
    """

    def __init__(self, name: str, age: int, email: str):
        """
        Constructs all the necessary attributes for the Person object.

        Parameters:
        ----------
        name : str
            The name of the person.
        age : int
            The age of the person.
        email : str
            The email address of the person.
        """
        self.name = name
        self.age = self.validate_age(age)
        self.email = email

    def introduce(self):
        """
        Prints a greeting message that includes the person's name and age.
        """
        print(f"Hi, my name is {self.name}, I am {self.age} years old.")

    @property
    def email(self):
        """Gets the email address of the person."""
        return self._email

    @email.setter
    def email(self, value):
        """
        Sets and validates the person's email address.

        Parameters:
        ----------
        value : str
            The email address to set.
        """
        self._email = self.validate_email(value)

    def validate_age(self, age: int):
        """
        Validates the age to ensure it is a non-negative integer.

        Parameters:
        ----------
        age : int
            The age to validate.

        Returns:
        -------
        int
            The validated age.

        Raises:
        ------
        ValueError:
            If the age is negative.
        """
        if age < 0:
            raise ValueError("Age cannot be negative.")
        return age

    def validate_email(self, email: str):
        """
        Validates the email address format.

        Parameters:
        ----------
        email : str
            The email address to validate.

        Returns:
        -------
        str
            The validated email address.

        Raises:
        ------
        ValueError:
            If the email format is invalid.
        """
        address = parseaddr(email)[1]
        if not address or "@" not in address:
            raise ValueError("Invalid email format.")
        return email


class Student(Person):
    """
    A class to represent a Student, inheriting from the Person class.

    Attributes:
    ----------
    student_id : str
        the unique student ID
    registered_courses : list
        a list of courses the student is registered for

    Methods:
    -------
    register_course(course: Course):
        Registers a student for a course.
    """

    def __init__(self, name: str, age: int, _email: str, student_id: str):
        """
        Constructs all the necessary attributes for the Student object.

        Parameters:
        ----------
        name : str
            The name of the student.
        age : int
            The age of the student.
        _email : str
            The student's email address.
        student_id : str
            The student's unique ID.
        """
        super().__init__(name, age, _email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course: "Course"):
        """
        Registers the student for a course.

        Parameters:
        ----------
        course : Course
            The course to register the student for.

        Raises:
        ------
        TypeError:
            If the course is not an instance of the Course class.
        """
        if isinstance(course, Course):
            self.registered_courses.append(course)
        else:
            raise TypeError("Only Course objects can be added.")


class Instructor(Person):
    """
    A class to represent an Instructor, inheriting from the Person class.

    Attributes:
    ----------
    instructor_id : str
        the unique instructor ID
    assigned_courses : list
        a list of courses the instructor is assigned to

    Methods:
    -------
    assign_course(course: Course):
        Assigns a course to the instructor.
    """

    def __init__(self, name: str, age: int, _email: str, instructor_id: str):
        """
        Constructs all the necessary attributes for the Instructor object.

        Parameters:
        ----------
        name : str
            The name of the instructor.
        age : int
            The age of the instructor.
        _email : str
            The instructor's email address.
        instructor_id : str
            The instructor's unique ID.
        """
        super().__init__(name, age, _email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course: "Course"):
        """
        Assigns the instructor to a course.

        Parameters:
        ----------
        course : Course
            The course to assign the instructor to.

        Raises:
        ------
        TypeError:
            If the course is not an instance of the Course class.
        """
        if isinstance(course, Course):
            self.assigned_courses.append(course)
        else:
            raise TypeError("Only Course objects can be added.")


class Course:
    """
    A class to represent a Course.

    Attributes:
    ----------
    course_id : str
        the unique course ID
    course_name : str
        the name of the course
    instructor : Instructor
        the instructor assigned to the course
    enrolled_students : list
        a list of students enrolled in the course

    Methods:
    -------
    add_student(student: Student):
        Adds a student to the course.
    """

    def __init__(self, course_id: str, course_name: str, instructor: "Instructor"):
        """
        Constructs all the necessary attributes for the Course object.

        Parameters:
        ----------
        course_id : str
            The unique course ID.
        course_name : str
            The name of the course.
        instructor : Instructor
            The instructor assigned to the course.

        Raises:
        ------
        TypeError:
            If the instructor is not an instance of the Instructor class.
        """
        if instructor is not None and not isinstance(instructor, Instructor):
            raise TypeError("Instructor must be an instance of Instructor class.")
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student: "Student"):
        """
        Adds a student to the course.

        Parameters:
        ----------
        student : Student
            The student to add to the course.

        Raises:
        ------
        TypeError:
            If the student is not an instance of the Student class.
        """
        if isinstance(student, Student):
            self.enrolled_students.append(student)
        else:
            raise TypeError("Only Student objects can be added.")


class DataManagement:
    """
    A class to manage data saving and loading in JSON and CSV formats.

    Methods:
    -------
    save_data(data, filename):
        Saves data to a JSON or CSV file.
    load_data(filename):
        Loads data from a JSON or CSV file.
    save_to_json(data, filename):
        Saves data to a JSON file.
    load_from_json(filename):
        Loads data from a JSON file.
    save_to_csv(data, filename):
        Saves data to a CSV file.
    load_from_csv(filename):
        Loads data from a CSV file.
    """

    @staticmethod
    def save_data(data, filename):
        """
        Saves the data to the specified file in either JSON or CSV format.

        Parameters:
        ----------
        data : list
            The data to be saved.
        filename : str
            The file to save the data to.

        Raises:
        ------
        ValueError:
            If the file format is not supported (only JSON and CSV are supported).
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".json":
            DataManagement.save_to_json(data, filename)
        elif ext == ".csv":
            DataManagement.save_to_csv(data, filename)
        else:
            raise ValueError("Unsupported file type. Only JSON and CSV are supported.")

    @staticmethod
    def load_data(filename):
        """
        Loads data from the specified file in either JSON or CSV format.

        Parameters:
        ----------
        filename : str
            The file to load the data from.

        Raises:
        ------
        ValueError:
            If the file format is not supported (only JSON and CSV are supported).

        Returns:
        -------
        list
            The loaded data.
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".json":
            return DataManagement.load_from_json(filename)
        elif ext == ".csv":
            return DataManagement.load_from_csv(filename)
        else:
            raise ValueError("Unsupported file type. Only JSON and CSV are supported.")

    @staticmethod
    def save_to_json(data, filename):
        """
        Saves data to a JSON file.

        Parameters:
        ----------
        data : list
            The data to be saved.
        filename : str
            The file to save the data to.
        """
        with open(filename, "w") as file:
            json.dump([obj.__dict__ for obj in data], file, indent=4)

    @staticmethod
    def load_from_json(filename):
        """
        Loads data from a JSON file.

        Parameters:
        ----------
        filename : str
            The file to load the data from.

        Returns:
        -------
        list
            The loaded data.
        """
        with open(filename, "r") as file:
            return json.load(file)

    @staticmethod
    def save_to_csv(data, filename):
        """
        Saves data to a CSV file.

        Parameters:
        ----------
        data : list of dict
            The data to be saved.
        filename : str
            The file to save the data to.

        Raises:
        ------
        ValueError:
            If the data is not in a suitable format for CSV.
        """
        if isinstance(data[0], dict):
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            raise ValueError("Data can't be saved to a csv file.")

    @staticmethod
    def load_from_csv(filename):
        """
        Loads data from a CSV file.

        Parameters:
        ----------
        filename : str
            The file to load the data from.

        Returns:
        -------
        list
            The loaded data as a list of dictionaries.
        """
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)
