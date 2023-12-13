from Department import *
from Student import *
from Major import *
from Course import *
from Section import *
from StudentMajor import *
from Enrollment import *


def create_collections(db):
    """
    create all the db collections, raise an exception for each in case it is already created.
    this can be implemented by just calling every schema creator. (really easy!)
    """

    pass


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


def department_index(db):
    departments = db["departments"]
    departments_index = departments.index_information()
    if "departments_names" in departments_index.keys():
        print("name index present.")
    else:
        departments.create_index(
            [("name", pymongo.ASCENDING)], unique=True, name="names"
        )

    if "departments_abbreviations" in departments_index.keys():
        print("abbreviation index present.")
    else:
        departments.create_index(
            [("abbreviation", pymongo.ASCENDING)],
            unique=True,
            name="departments_abbreviations",
        )

    if "departments_chair_names" in departments_index.keys():
        print("chair name index present.")
    else:
        departments.create_index(
            [("chair_name", pymongo.ASCENDING)],
            unique=True,
            name="departments_chair_names",
        )

    if "departments_office_buildings" in departments_index.keys():
        print("office building index present.")
    else:
        departments.create_index(
            [("building", pymongo.ASCENDING), ("office", pymongo.ASCENDING)],
            unique=True,
            name="departments_office_buildings",
        )

    if "departments_descriptions" in departments_index.keys():
        print("description index present.")
    else:
        departments.create_index(
            [("description", pymongo.ASCENDING)],
            unique=True,
            name="departments_descriptions",
        )


def course_index(db):
    courses = db["courses"]
    courses_index = courses.index_information()
    if "courses_numbers" in courses_index.keys():
        print("number and department abbreviation index present.")
    else:
        courses.create_index(
            [
                ("course_number", pymongo.ASCENDING),
                ("department_abbreviation", pymongo.ASCENDING),
            ],
            unique=True,
            name="courses_numbers",
        )
    if "courses_names" in courses_index.keys():
        print("number index present.")
    else:
        courses.create_index(
            [
                ("name", pymongo.ASCENDING),
                ("department_abbreviation", pymongo.ASCENDING),
            ],
            unique=True,
            name="courses_names",
        )


def section_index(db):
    sections = db["sections"]
    sections_index = sections.index_information()
    if "sections_pks1" in sections_index.keys():
        print("pks index present.")
    else:
        sections.create_index(
            [
                ("course_number", pymongo.ASCENDING),
                ("section_number", pymongo.ASCENDING),
                ("semester", pymongo.ASCENDING),
                ("section_year", pymongo.ASCENDING),
            ],
            unique=True,
            name="sections_pks1",
        )
    if "sections_buildings" in sections_index.keys():
        print("buildings index present.")
    else:
        sections.create_index(
            [
                ("semester", pymongo.ASCENDING),
                ("section_year", pymongo.ASCENDING),
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
                ("semester", pymongo.ASCENDING),
                ("section_year", pymongo.ASCENDING),
                ("schedule", pymongo.ASCENDING),
                ("start_time", pymongo.ASCENDING),
                ("instructor", pymongo.ASCENDING),
            ],
            unique=True,
            name="sections_instructors",
        )


def student_index(db):
    students = db["students"]
    students_indexes = students.index_information()
    if "students_last_and_first_names" in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index(
            [("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)],
            unique=True,
            name="students_last_and_first_names",
        )
    if "students_e_mail" in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index(
            [("e_mail", pymongo.ASCENDING)], unique=True, name="students_e_mail"
        )
    pprint(students.index_information())


def major_index(db):
    majors = db["majors"]
    majors_indexes = majors.index_information()
    if "majors_names" in majors_indexes.keys():
        print("major name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        majors.create_index(
            [("name", pymongo.ASCENDING)],
            unique=True,
            name="majors_names",
        )


def student_major_index(db):
    students_majors = db["student_major"]
    students_majors_indexes = students_majors.index_information()
    if "stundets_majors_ids" in students_majors_indexes.keys():
        print("student major student id index present.")
    else:
        students_majors.create_index(
            [("student_id", pymongo.ASCENDING), ("section_id", pymongo.ASCENDING)],
            unique=True,
            name="stundets_majors_ids",
        )


def enrollment_index(db):
    enrollments = db["enrollment"]
    enrollments_indexes = enrollments.index_information()
    if "enrollemnts_ids" in enrollments_indexes.keys():
        print("enrollment student id index present.")
    else:
        enrollments.create_index(
            [("student_id", pymongo.ASCENDING), ("section_id", pymongo.ASCENDING)],
            unique=True,
            name="enrollemnts_ids",
        )
    if "enrollments_types" in enrollments_indexes.keys():
        print("enrollment type index present.")
    else:
        enrollments.create_index(
            [("enrollment_type", pymongo.ASCENDING)],
            unique=True,
            name="enrollments_types",
        )


if __name__ == "__main__":
    config = ConfigParser()
    config.sections()
    config.read("config.config")
    print(config["Mongo"]["USERNAME"])
    username = config["Mongo"]["USERNAME"]
    password = config["Mongo"]["PASSWORD"]
    project = config["Mongo"]["PROJECT"]
    hash_name = config["Mongo"]["HASH"]
    database_name = (
        input("database name (press ENTER for 'Demonstration')-->") or "Demonstration"
    )  # just press enter :/
    # password: str = getpass.getpass('Mongo DB password -->')
    # username: str = input('Database username [user on Atlas] -->') or \
    #                 "CECS-323-Spring-2023-user"
    # project: str = input('Mongo project name [Atlas Project Name] -->') or \
    #                "CECS-323-Spring-2023"
    # hash_name: str = input('7-character database hash [qzl49vl] -->') or "puxnikb"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(
        f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    )
    client = MongoClient(cluster)
    db = client[database_name]
    # As a test that the connection worked, print out the database names.
    try:
        create_collections(db)
    except Exception as e:
        pprint(f"Collections not created. Error: {e}")

    print(client.list_database_names())

    try:
        department_index(db)
        course_index(db)
        section_index(db)
        student_index(db)
        major_index(db)
        student_major_index(db)
        enrollment_index(db)
    except Exception as e:
        pprint(f"Indexes not created. Error: {e}")

    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)
