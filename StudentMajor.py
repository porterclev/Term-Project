from datetime import datetime
from Student import *
from Major import *

def add_student_major(db):
    majors = db["majors"]
    students = db["students"]
    student_majors = db["student_majors"]


    while True:
        student = select_student(db)
        major = select_major(db)
        declaration_date = datetime(input("declaration date-->"))
        if declaration_date > datetime.today():
            print("date must be today or earlier!!")
            continue
        try:
            student_major = {"student_id": student["_id"],
                             "major_id": major["_id"],
                             "declaration_date": declaration_date}
            student_majors.insert_one(student_major)
            print("successfully inserted!")
        except Exception as e:
            pprint(f"Insert failed. Error: {e}")


def select_student_major(db):
    while True:

        major = select_major(db)
        student = select_student(db)
        student_majors = db["student_majors"]
        student_major = student_majors.find_one({"student_id": student["_id"],
                                          "major_id": major["_id"]
                                           })
        if student_major is not None:
            return student_major
        else:
            print("no such student_major!")


def delete_student_major(db):
    student_major = select_student_major(db)
    student_majors = db["student_majors"]

    student_major.delete_one(student_majors)


def list_student_major(db):
    students = (
        db["students"]
        .find({})
        .sort([("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)])
    )
    majors = db["majors"]

    for student in students:

        student_majors = (
            db["student_majors"]
            .find({"student_id": student["_id"]})
        )
        if student_majors is not None:
            pprint(f'{student["first_name"]} {student["last_name"]} Majors:')
        for student_major in student_majors:

            major = majors.find_one({"_id": student_major["major_id"]})
            pprint(major)