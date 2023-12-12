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
from Student import *
from Section import *

def add_pass_fail(db):
    enrollments = db["enrollments"]
    students = db["students"]
    sections = db["sections"]
    pass_fails = db["pass_fails"]

    student = select_student(db)
    section = select_section(db)
    while True:
        application_date = datetime(input("application date-->"))
        try:
            enrollment = {"student_id": student["_id"],
                          "section_id": section["_id"]}
            enrollments.insert_one(enrollment)
        except Exception as e:
            pprint(f"Insert failed for enrollment. Error: {e}")



def add_letter_grade(db):
    pass

def select_enrollment(db):
    pass
def list_enrollment(db):
    pass
def delete_enrollment(db):
    pass

