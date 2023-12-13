import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from configparser import ConfigParser
from Department import *

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

def select_course(db):
    department = select_department(db)
    courses = db["courses"]
    while True:
        course_number = int(input("course number-->"))

        if courses.count_documents({"course_number": course_number}) > 0:
            course_found = courses.find_one({"course_number": course_number})
            return course_found
        else:
            print(f"{course_number} not found in department {department['abbreviation']}")


def add_course(db):
    while True:
        collection = db["courses"]
        unique_department_abbreviation = False
        unique_course_number = False
        unique_course_name = False
        unique_course_description = False
        department_abbreviation: str = ""
        course_number = 0
        course_name = ""
        course_description = ""
        department_abbreviation = input("Enter the department abbreviation: ")
        if (
            db["departments"].count_documents({"abbreviation": department_abbreviation})
            == 0
        ):
            print("Department abbreviation does not exist. Please try again.")
            continue
        course_number = int(input("Enter the course number: "))
        course_name = input("Enter the course name: ")
        course_description = input("Enter the course description: ")
        for course in collection.find():
            if course["department_abbreviation"] == department_abbreviation:
                unique_department_abbreviation = True
            if course["course_number"] == course_number:
                unique_course_number = True
            if course["course_name"] == course_name:
                unique_course_name = True
            if course["course_description"] == course_description:
                unique_course_description = True
        if unique_department_abbreviation and unique_course_number:
            print("Course already exists. Please try again.")
            continue
        if unique_course_name:
            print("Course name already exists. Please try again.")
            continue
        if unique_course_description:
            print("Course description already exists. Please try again.")
            continue

        try:
            result = collection.insert_one(
                {
                    "department_abbreviation": department_abbreviation,
                    "course_number": course_number,
                    "course_name": course_name,
                    "course_description": course_description,
                }
            )
            print("Course added successfully.")
        except Exception as e:
            pprint(f"Insert Failed. Error: {e}")
        else:
            break



def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    if db["sections"].count_documents({"course_number": course["course_number"],
                                       "department_abbreviation": course["department_abbreviation"]
                                       }) > 0:
        print("that course contains sections!!!")
    else:
        try:
            deleted = courses.delete_one({"_id": course["_id"]})
            print(f"We just deleted: {deleted.deleted_count} courses.")
        except Exception as e:
            pprint(f"Delete Failed. Error: {e}")


def list_course(db):
    courses = db["courses"].find({}).sort([("department_abbreviation", pymongo.ASCENDING), ("course_number", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)

