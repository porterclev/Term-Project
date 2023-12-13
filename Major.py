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



def add_major(db):
    department = select_department(db)
    majors = db["majors"]
    while True:

        name = input("name-->")
        description = input("description-->")
        try:
            major = {"department_abbreviation": department["abbreviation"],
                     "name": name,
                     "description": description}
            results = majors.insert_one(major)
            break
        except Exception as e:
            pprint(f"Insert failed. Error: {e}")

def select_major(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    majors = db["majors"]
    found: bool = False
    name: str = ""
    description: str = ""
    while not found:
        name = input("major name--> ")
        name_count: int = majors.count_documents(
            {"name": name}
        )
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    found_student = majors.find_one({"name": name})
    return found_student


def delete_major(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    major = select_major(db)
    # Create a "pointer" to the students collection within the db database.
    majors = db["majors"]
    # student["_id"] returns the _id value from the selected student document.
    student_majors = db["student_majors"]
    if student_majors.count_documents({"major_id": major["_id"]}) > 0:
        pprint("that major has students in it!!!")
    else:
        try:
            deleted = majors.delete_one({"_id": major["_id"]})
            print(f"We just deleted: {deleted.deleted_count} major(s).")
        except Exception as e:
            pprint(f"delete failed. Error: {e}")
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.



def list_major(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    majors = (
        db["majors"]
        .find({})
        .sort([("name", pymongo.ASCENDING), ("description", pymongo.ASCENDING)])
    )
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for major in majors:
        pprint(major)


