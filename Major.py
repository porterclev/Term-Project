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


def add_major(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.

    collection = db["majors"]
    unique_name = False
    unique_description = False
    name: str = ""
    description: str = ""
    while not unique_name or not unique_description:
        name = input("major name--> ")
        description = input("major description--> ")
        name_count: int = collection.count_documents(
            {"name": name, "description": description}
        )
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            description = collection.count_documents({"description": description})
            unique_description = description == 0
            if not unique_description:
                print("We already have a student with that e-mail address.  Try again.")
    # Build a new students document preparatory to storing it
    major = {"name": name, "description": description}
    results = collection.insert_one(major)


def select_major(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["majors"]
    found: bool = False
    name: str = ""
    description: str = ""
    while not found:
        name = input("Student's last name--> ")
        description = input("Student's first name--> ")
        name_count: int = collection.count_documents(
            {"name": name, "description": description}
        )
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"name": name, "description": description})
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
    deleted = majors.delete_one({"_id": major["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} students.")


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


if __name__ == "__main__":
    config = ConfigParser()
    config.sections()
    config.read("config.config")
    print(config["Mongo"]["USERNAME"])
    username = config["Mongo"]["USERNAME"]
    password = config["Mongo"]["PASSWORD"]
    project = config["Mongo"]["PROJECT"]
    hash_name = config["Mongo"]["HASH"]

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
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # ************************** Set up the students collection
    students_indexes = students.index_information()
    if "majors_names" in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index(
            [("major_name", pymongo.ASCENDING), ("majors_names", pymongo.ASCENDING)],
            unique=True,
            name="majors_names",
        )
    if "majors_descriptions" in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index(
            [("major_description", pymongo.ASCENDING)],
            unique=True,
            name="majors_descriptions",
        )
    pprint(students.index_information())
    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)
