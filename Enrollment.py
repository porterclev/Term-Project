import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from configparser import ConfigParser
from datetime import time, datetime

def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ""
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ""
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ""
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

def add_enrollment(db):
    collection = db["enrollments"]
    unique_student: bool = False
    unique_section: bool = False
    studentID: str = ""
    sectionID: str = ""
    enrollmentType: str = ""
    while not unique_student and not unique_section:
        studentID = input("Student ID--> ")
        sectionID = input("Section ID--> ")
        student_count: int = collection.count_documents(
            {"student_id": studentID})
        unique_name = name_count == 0
        section_count = collection.count_documents({"section_id": sectionID})
        unique_email = email_count == 0     
        if not unique_name and not unique student:
            print("We already have a student with that ID number enrolled in that section.  Try again.")          
    while enrollmentType not in ["PassFail", "LetterGrade"]:
        enrollmentType = input("Enrollement type--> ")
        if enrollmentType not in ["PassFail", "LetterGrade"]:
            print("Enrollment type must be PassFail or LetterGrade.")        
    enrollment = {"student_id": studentID, "section_id": sectionID, "enrollment_type": enrollmentType}
    results = collection.insert_one(enrollment)

def delete_enrollment(db):
    collection = db["enrollments"]
    while True:
        section_id = int(input("Enter the section ID of the enrollment to delete: "))
        unique_section_id = False
        student_id = int(input("Enter the student ID of the enrollment to delete: "))
        unique_student_id = False
        for enrollment in collection.find():
            if enrollment["section_id"] == section_id:
                unique_section_id = True
            if enrollment["course_number"] == course_number:
                unique_student_id = True

