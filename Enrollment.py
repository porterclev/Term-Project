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
import datetime
from Student import *
from Section import *

def add_pass_fail(db):
    enrollments = db["enrollments"]
    students = db["students"]
    sections = db["sections"]
    pass_fails = db["pass_fails"]


    while True:
        student = select_student(db)
        section = select_section(db)
        application_date = datetime(input("application date-->"))
        if application_date > datetime.today():
            print("date must be today or earlier!!")
            continue
        try:
            enrollment = {"student_id": student["_id"],
                          "section_id": section["_id"]}
            enrollments.insert_one(enrollment)
        except Exception as e:
            pprint(f"Insert failed for enrollment. Error: {e}")
        else:
            try:
                tmp_enroll = enrollments.find_one({"student_id": student["_id"],
                                                   "section_id": section["_id"]
                                                   })
                pass_fail = {"enrollment_id": tmp_enroll["_id"],
                             "application_date": application_date}
                pass_fails.add_one(pass_fail)
                return enrollment
            except Exception as e:
                pprint(f"Insert failed for pass_fail. Error: {e}")



def add_letter_grade(db):
    def add_pass_fail(db):
        enrollments = db["enrollments"]
        students = db["students"]
        sections = db["sections"]
        letter_grades = db["pass_fails"]


        while True:
            student = select_student(db)
            section = select_section(db)
            min_satisfactory = datetime(input("minimum satisfactory grade-->"))
            try:
                enrollment = {"student_id": student["_id"],
                              "section_id": section["_id"]}
                enrollments.insert_one(enrollment)
            except Exception as e:
                pprint(f"Insert failed for enrollment. Error: {e}")
                continue
            else:
                try:
                    tmp_enroll = enrollments.find_one({"student_id": student["_id"],
                                                       "section_id": section["_id"]
                                                       })
                    letter_grade = {"enrollment_id": tmp_enroll["_id"],
                                    "min_satisfactory": min_satisfactory}
                    letter_grades.add_one(letter_grade)
                    return enrollment
                except Exception as e:
                    pprint(f"Insert failed for letter_grade. Error: {e}")

def select_enrollment(db):
    while True:

        section = select_section(db)
        student = select_student(db)
        enrollments = db["enrollments"]
        enrollment = enrollments.find_one({"student_id": student["_id"],
                                          "section_id": section["_id"]
                                           })
        if enrollment is not None:
            return enrollment
        else:
            print("no such enrollment!!")

def list_enrollment(db):
    students = (
        db["students"]
        .find({})
        .sort([("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)])
    )
    sections = db["sections"]
    pass_fails = db["pass_fails"]
    letter_grades = db["letter_grades"]

    for student in students:

        enrollments = (
                        db["enrollments"]
                        .find({"student_id": student["_id"]})
                    )
        if enrollments is not None:
            pprint(f'{student["first_name"]} {student["last_name"]} Enrollments:')
        for enrollment in enrollments:
            section = sections.find_one({"_id": enrollment["section_id"]})
            pprint(section)
            pass_fail = pass_fails.find_one({"enrollment_id": enrollment["_id"]})
            letter_grade = letter_grades.find_one({"enrollment_id": enrollment["_id"]})
            if pass_fail is not None:
                pprint(pass_fail["application_date"])
            else:
                pprint(letter_grade["min_satisfactory"])




def delete_enrollment(db):
    enrollment = select_enrollment(db)
    enrollments = db["enrollment"]
    pass_fails = db["pass_fails"]
    letter_grades = db["letter_grades"]

    for pass_fail in pass_fails.find({"enrollment_id": enrollment["_id"]}):
        pass_fails.delete_one(pass_fail)
    for letter_grade in letter_grades.find({"enrollment_id": enrollment["_id"]}):
        letter_grades.delete_one(letter_grade)
    enrollments.delete_one(enrollment)

