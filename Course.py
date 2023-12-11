import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from configparser import ConfigParser


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
        break
    result = collection.insert_one(
        {
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "course_name": course_name,
            "course_description": course_description,
        }
    )
    print("Course added successfully.")


def delete_course(db):
    collection = db["courses"]
    while True:
        course_number = input("Enter the course number to delete: ")
        unique_course_number = False
        for course in collection.find():
            if course["course_number"] == course_number:
                unique_course_number = True
        if not unique_course_number:
            print("Course number does not exist. Please try again.")
            continue
        break
    result = collection.delete_one({"course_number": course_number})
    print("Course deleted successfully.")


def list_course(db):
    collection = db["courses"]
    for course in collection.find():
        print(course)


if __name__ == "__main__":
    config = ConfigParser()
    config.sections()
    config.read("config.config")
    print(config["Mongo"]["USERNAME"])
    username = config["Mongo"]["USERNAME"]
    password = config["Mongo"]["PASSWORD"]
    project = config["Mongo"]["PROJECT"]
    hash_name = config["Mongo"]["HASH"]
    # password: str = getpass.getpass("Mongo DB password -->")
    # username: str = (
    #     input("Database username [user on Atlas] -->") or "CECS-323-Spring-2023-user"
    # )
    # project: str = (
    #     input("Mongo project name [Atlas Project Name] -->") or "CECS-323-Spring-2023"
    # )
    # hash_name: str = input("7-character database hash [qzl49vl] -->") or "puxnikb"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(
        f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    )
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    courses = db["courses"]
    course_count = courses.count_documents({})
    print(f"Courses in the collection so far: {course_count}")

    # ************************** Set up the students collection
    courses_index = courses.index_information()
    if "courses_names" in courses_index.keys():
        print("name index present.")
    else:
        courses.create_index(
            [
                ("course_name", pymongo.ASCENDING),
                ("department_abbreviation", pymongo.ASCENDING),
            ],
            unique=True,
            name="courses_names",
        )

    # if "courses_departments" in courses_index.keys():
    #     print("department index present.")
    # else:
    #     courses.create_index(
    #         [("department_abbreviation", pymongo.ASCENDING)],
    #         unique=True,
    #         name="courses_departments",
    #     )

    if "courses_numbers" in courses_index.keys():
        print("number index present.")
    else:
        courses.create_index(
            [("course_number", pymongo.ASCENDING)],
            unique=True,
            name="courses_numbers",
        )

    if "courses_descriptions" in courses_index.keys():
        print("chair name index present.")
    else:
        courses.create_index(
            [("course_description", pymongo.ASCENDING)],
            unique=True,
            name="description",
        )

    pprint(courses.index_information())
    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)
