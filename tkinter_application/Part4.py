"""
Database Module for School Management System

This module provides the Database class, which handles all interactions with the SQLite
database for the School Management System. It includes methods for creating tables,
adding, updating, deleting, and retrieving records related to students, instructors,
courses, and registrations.

Dependencies:
    - sqlite3: For interacting with the SQLite database.
    - typing: For type annotations.
    - Part1: Contains the Course, Instructor, and Student classes.

Classes:
    Database: Manages all database operations including CRUD for students, instructors,
             courses, and registrations.
"""

import sqlite3
from typing import List, Optional, Tuple

from Part1 import Course, Instructor, Student


class Database:
    """
    Database management for the School Management System.

    This class provides methods to create necessary tables and perform CRUD operations
    on students, instructors, courses, and registrations within an SQLite database.
    It ensures data integrity through the use of primary keys and foreign keys.
    """

    def __init__(self, db_name: str = "school.db"):
        """
        Initialize the Database instance and create tables if they do not exist.

        Args:
            db_name (str, optional): The name of the SQLite database file. Defaults to "school.db".
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create the necessary tables for students, instructors, courses, and registrations.

        This method ensures that all required tables are present in the database with
        appropriate constraints such as primary keys, foreign keys, and unique fields.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                instructor_id TEXT,
                FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id),
                UNIQUE(student_id, course_id)
            )
            """
        )

        self.conn.commit()

    def add_student(self, student: Student) -> bool:
        """
        Add a new student to the database.

        Args:
            student (Student): The Student instance to be added.

        Returns:
            bool: True if the student was added successfully, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO students (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (student.student_id, student.name, student.age, student.email),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding student: {e}")
            return False

    def add_instructor(self, instructor: Instructor) -> bool:
        """
        Add a new instructor to the database.

        Args:
            instructor (Instructor): The Instructor instance to be added.

        Returns:
            bool: True if the instructor was added successfully, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (
                    instructor.instructor_id,
                    instructor.name,
                    instructor.age,
                    instructor.email,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding instructor: {e}")
            return False

    def add_course(self, course: Course) -> bool:
        """
        Add a new course to the database.

        Args:
            course (Course): The Course instance to be added.

        Returns:
            bool: True if the course was added successfully, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO courses (course_id, course_name, instructor_id)
                VALUES (?, ?, ?)
                """,
                (
                    course.course_id,
                    course.course_name,
                    course.instructor.instructor_id if course.instructor else None,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding course: {e}")
            return False

    def register_student_to_course(self, student_id: str, course_id: str) -> bool:
        """
        Register a student to a course.

        Args:
            student_id (str): The ID of the student.
            course_id (str): The ID of the course.

        Returns:
            bool: True if the registration was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                SELECT * FROM registrations
                WHERE student_id = ? AND course_id = ?
                """,
                (student_id, course_id),
            )
            if self.cursor.fetchone():
                print("Student is already registered for this course.")
                return False

            self.cursor.execute(
                """
                INSERT INTO registrations (student_id, course_id)
                VALUES (?, ?)
                """,
                (student_id, course_id),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error registering student to course: {e}")
            return False

    def assign_instructor_to_course(self, instructor_id: str, course_id: str) -> bool:
        """
        Assign an instructor to a course.

        Args:
            instructor_id (str): The ID of the instructor.
            course_id (str): The ID of the course.

        Returns:
            bool: True if the assignment was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                "SELECT * FROM instructors WHERE instructor_id = ?", (instructor_id,)
            )
            instructor = self.cursor.fetchone()
            if not instructor:
                print(f"Instructor ID {instructor_id} does not exist.")
                return False

            self.cursor.execute(
                "SELECT * FROM courses WHERE course_id = ?", (course_id,)
            )
            course = self.cursor.fetchone()
            if not course:
                print(f"Course ID {course_id} does not exist.")
                return False

            self.cursor.execute(
                """
                UPDATE courses
                SET instructor_id = ?
                WHERE course_id = ?
                """,
                (instructor_id, course_id),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error assigning instructor to course: {e}")
            return False

    def get_students(self) -> List[Tuple]:
        """
        Retrieve all students from the database.

        Returns:
            List[Tuple]: A list of tuples, each representing a student record.
        """
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_instructors(self) -> List[Tuple]:
        """
        Retrieve all instructors from the database.

        Returns:
            List[Tuple]: A list of tuples, each representing an instructor record.
        """
        self.cursor.execute("SELECT * FROM instructors")
        return self.cursor.fetchall()

    def get_courses(self) -> List[Tuple]:
        """
        Retrieve all courses from the database.

        Returns:
            List[Tuple]: A list of tuples, each representing a course record.
        """
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id: str) -> Optional[Tuple]:
        """
        Retrieve a student by their ID.

        Args:
            student_id (str): The ID of the student.

        Returns:
            Optional[Tuple]: The student record as a tuple if found, None otherwise.
        """
        self.cursor.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        )
        return self.cursor.fetchone()

    def get_course_by_id(self, course_id: str) -> Optional[Tuple]:
        """
        Retrieve a course by its ID.

        Args:
            course_id (str): The ID of the course.

        Returns:
            Optional[Tuple]: The course record as a tuple if found, None otherwise.
        """
        self.cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        return self.cursor.fetchone()

    def get_instructor_by_id(self, instructor_id: str) -> Optional[Tuple]:
        """
        Retrieve an instructor by their ID.

        Args:
            instructor_id (str): The ID of the instructor.

        Returns:
            Optional[Tuple]: The instructor record as a tuple if found, None otherwise.
        """
        self.cursor.execute(
            "SELECT * FROM instructors WHERE instructor_id = ?", (instructor_id,)
        )
        return self.cursor.fetchone()

    def get_student_courses(self, student_id: str) -> List[Tuple]:
        """
        Retrieve all courses a student is registered for.

        Args:
            student_id (str): The ID of the student.

        Returns:
            List[Tuple]: A list of tuples, each representing a course the student is registered for.
        """
        self.cursor.execute(
            """
            SELECT c.course_id, c.course_name
            FROM courses c
            JOIN registrations r ON c.course_id = r.course_id
            WHERE r.student_id = ?
            """,
            (student_id,),
        )
        return self.cursor.fetchall()

    def update_student(self, student: Student) -> bool:
        """
        Update a student's information in the database.

        Args:
            student (Student): The Student instance with updated information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                UPDATE students
                SET name = ?, age = ?, email = ?
                WHERE student_id = ?
                """,
                (student.name, student.age, student.email, student.student_id),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating student: {e}")
            return False

    def update_instructor(self, instructor: Instructor) -> bool:
        """
        Update an instructor's information in the database.

        Args:
            instructor (Instructor): The Instructor instance with updated information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                UPDATE instructors
                SET name = ?, age = ?, email = ?
                WHERE instructor_id = ?
                """,
                (
                    instructor.name,
                    instructor.age,
                    instructor.email,
                    instructor.instructor_id,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating instructor: {e}")
            return False

    def update_course(self, course: Course) -> bool:
        """
        Update a course's information in the database.

        Args:
            course (Course): The Course instance with updated information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                UPDATE courses
                SET course_name = ?, instructor_id = ?
                WHERE course_id = ?
                """,
                (
                    course.course_name,
                    course.instructor.instructor_id if course.instructor else None,
                    course.course_id,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating course: {e}")
            return False

    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student from the database.

        Args:
            student_id (str): The ID of the student to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                "DELETE FROM students WHERE student_id = ?", (student_id,)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error deleting student: {e}")
            return False

    def delete_instructor(self, instructor_id: str) -> bool:
        """
        Delete an instructor from the database.

        Args:
            instructor_id (str): The ID of the instructor to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                "DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error deleting instructor: {e}")
            return False

    def delete_course(self, course_id: str) -> bool:
        """
        Delete a course from the database.

        Args:
            course_id (str): The ID of the course to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error deleting course: {e}")
            return False

    def close(self):
        """
        Close the database connection.

        This method should be called when the database operations are complete to ensure
        that all resources are properly released.
        """
        self.conn.close()
