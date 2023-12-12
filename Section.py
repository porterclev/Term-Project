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


def add_section(db):
    while True:
        collection = db["sections"]
        unique_pk: bool = False
        unique_building: bool = False
        unique_instructor: bool = False
        department_abbreviation: str = ""
        course_number: int
        section_number: int
        semester: str = ""
        section_year: int
        building: str = ""
        room: int
        schedule: str = ""
        start_time: str = ""
        instructor: str = ""

        print("Please provide the course that this section belongs to:")
        department_abbreviation = input("Department abbreviation --> ")
        # if (
        #     db["departments"].count_documents({"abbreviation": department_abbreviation})
        #     == 0
        # ):
        #     print("Department abbreviation does not exist. Please try again.")
        #     continue
        course_number = int(input("Course number --> "))
        if (
            db["courses"].count_documents(
                {
                    "department_abbreviation": department_abbreviation,
                    "course_number": course_number,
                }
            )
            == 0
        ):
            print("Course Number does not exist. Please try again.")
            continue
        section_number = int(input("What is the section number -->"))
        semester = input("Which semester is this section offered in? --> ")
        section_year = int(input("Which year is this section offered in? --> "))
        building = input("Which building is this section offered in? --> ")
        room = int(
            input(f"Which room of building {building} is this section offered in? --> ")
        )
        schedule = input("What is the schedule for this section? (MW, MWF)--> ")
        # start_hour = int(input("Start hour --> "))
        # start_minute = int(input("Start minute --> "))
        start_time = input("Start time --> ")
        instructor = input("Instructor full name --> ")
        for section in collection.find():
            if (
                section["department_abbreviation"] == department_abbreviation
                and section["course_number"] == course_number
                and section["section_number"] == section_number
                and section["semester"] == semester
                and section["section_year"] == section_year
            ):
                unique_pk = True
            if (
                section["section_number"] == section_number
                and section["semester"] == semester
                and section["building"] == building
                and section["room"] == room
                and section["schedule"] == schedule
                and section["start_time"] == start_time
            ):
                unique_building = True
            if (
                section["section_number"] == section_number
                and section["semester"] == semester
                and section["start_time"] == start_time
                and section["instructor"] == instructor
            ):
                unique_instructor = True

        if unique_pk:
            print("Section name already exists. Please try again.")
            continue
        if unique_building:
            print("Section with that building already exists. Please try again.")
            continue
        if unique_instructor:
            print("Section with that instructor already exists. Please try again.")
            continue
        break
    result = collection.insert_one(
        {
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year,
            "building": building,
            "room": room,
            "schedule": schedule,
            "start_time": start_time,
            "instructor": instructor,
        }
    )
    print("section added successfully.")


def delete_section(db):
    collection = db["sections"]
    while True:
        department_abbreviation = input("Enter the department abbreviation to delete: ")
        unique_department_abbreviation = False
        course_number = int(input("Enter the course number to delete: "))
        unique_course_number = False
        section_number = int(input("Enter the section number to delete: "))
        unique_section_number = False
        semester = input("Enter the semester to delete: ")
        unique_semester = False
        section_year = int(input("Enter the section year to delete: "))
        unique_section_year = False
        for section in collection.find():
            if section["department_abbreviation"] == department_abbreviation:
                unique_department_abbreviation = True
            if section["course_number"] == course_number:
                unique_course_number = True
            if section["section_number"] == section_number:
                unique_section_number = True
            if section["semester"] == semester:
                unique_semester = True
            if section["section_year"] == section_year:
                unique_section_year = True

        if (
            not unique_course_number
            and not unique_department_abbreviation
            and not unique_section_number
            and not unique_semester
            and not unique_section_year
        ):
            print("Course number does not exist. Please try again.")
            continue
        break
    result = collection.delete_one(
        {
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year,
        }
    )
    print("Course deleted successfully.")


def list_section(db):
    collection = db["sections"]
    for section in collection.find():
        print(section)


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
    sections = db["sections"]
    course_count = sections.count_documents({})
    print(f"Departments in the collection so far: {course_count}")

    # ************************** Set up the students collection
    sections_index = sections.index_information()
    if "sections_pks" in sections_index.keys():
        print("pks index present.")
    else:
        sections.create_index(
            [
                ("department_abbreviation", pymongo.ASCENDING),
                ("course_number", pymongo.ASCENDING),
                ("section_number", pymongo.ASCENDING),
                ("semester", pymongo.ASCENDING),
                ("section_year", pymongo.ASCENDING),
            ],
            unique=True,
            name="sections_pks",
        )
    if "sections_buildings" in sections_index.keys():
        print("buildings index present.")
    else:
        sections.create_index(
            [
                ("section_number", pymongo.ASCENDING),
                ("semester", pymongo.ASCENDING),
                ("building", pymongo.ASCENDING),
                ("room", pymongo.ASCENDING),
                ("schedule", pymongo.ASCENDING),
                ("start_time", pymongo.ASCENDING),
            ],
            unique=True,
            name="sections_buildings",
        )

    if "sections_instructors" in sections_index.keys():
        print("instructors index present.")
    else:
        sections.create_index(
            [
                ("section_number", pymongo.ASCENDING),
                ("semester", pymongo.ASCENDING),
                ("start_time", pymongo.ASCENDING),
                ("instructor", pymongo.ASCENDING),
            ],
            unique=True,
            name="sections_instructors",
        )
    """ if "sections_course_numbers" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("course_number", pymongo.ASCENDING)],
            unique=True,
            name="sections_course_numbers",
        )

    if "sections_section_numbers" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_section_number", pymongo.ASCENDING)],
            unique=True,
            name="sections_section_numbers",
        )

    if "sections_semesters" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_semester", pymongo.ASCENDING)],
            unique=True,
            name="sections_semesters",
        )

    if "sections_section_years" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_section_year", pymongo.ASCENDING)],
            unique=True,
            name="sections_section_years",
        )

    if "sections_buildings" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_building", pymongo.ASCENDING)],
            unique=True,
            name="sections_buildings",
        )

    if "sections_rooms" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_room", pymongo.ASCENDING)],
            unique=True,
            name="sections_rooms",
        )

    if "sections_schedules" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_schedule", pymongo.ASCENDING)],
            unique=True,
            name="sections_schedules",
        )

    if "sections_start_times" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_start_time", pymongo.ASCENDING)],
            unique=True,
            name="sections_start_times",
        )

    if "sections_instructors" in sections_index.keys():
        print("name index present.")
    else:
        sections.create_index(
            [("section_instructor", pymongo.ASCENDING)],
            unique=True,
            name="sections_instructors",
        ) """

    pprint(sections.index_information())
    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)
