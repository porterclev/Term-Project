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


def add_department(db):
    while True:
        # Create a "pointer" to the students collection within the db database.
        collection = db["departments"]
        unique_abbreviation: bool = False
        unique_chair_name: bool = False
        unique_office_building: bool = False
        unique_description: bool = False
        name: str = ""
        abbreviation: str = ""
        chair_name: str = ""
        building: str = ""
        office: int = -1
        description: str = ""
        while (
            not unique_abbreviation
            or not unique_description
            or not unique_office_building
            or not unique_chair_name
        ):
            name = input("Department name--> ")
            abbreviation = input("Department abbreviation--> ")
            abbreviation_count: int = collection.count_documents(
                {"abbreviation": abbreviation}
            )
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have that abbreviation  Try again.")
                continue
            chair_name = input("Department chair name--> ")
            chair_name_count = collection.count_documents({"chair_name": chair_name})
            unique_chair_name = chair_name_count == 0
            if not unique_chair_name:
                print("We already have that chair_name  Try again.")
                continue
            building = input("Department office building--> ")
            office = int(input("Department office number--> "))
            office_building_count = collection.count_documents(
                {"building": building, "office": office}
            )
            unique_office_building = office_building_count == 0
            if not unique_office_building:
                print("We already have that office building  Try again.")
                continue
            description = input("Department description--> ")
            description_count = collection.count_documents({"description": description})
            unique_description = description_count == 0
            if not unique_description:
                print("We already have that description  Try again.")
                continue
            print()
        try:
            # Build a new students document preparatory to storing it
            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chair_name,
                "building": building,
                "office": office,
                "description": description,
            }
            results = collection.insert_one(department)
            break
        except Exception as e:
            print(f"Insert failed.  Error: {e}")


def select_department(db):
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ""
    chair_name: str = ""
    building: str = ""
    office: int = -1
    description: str = ""
    while not found:
        abbreviation = input("Department abbreviation--> ")
        abb_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abb_count == 1
        if not found:
            print("No department found by that abbreviation.  Try again.")
            continue

        found = False
        chair_name = input("Department chair name--> ")
        chair_count: int = collection.count_documents({"chair_name": chair_name})
        found = chair_count == 1
        if not found:
            print("No department found with that chair name.  Try again.")
            continue

        found = False
        building = input("Department office building--> ")
        office = int(input("Department office number--> "))
        building_count: int = collection.count_documents(
            {"building": building, "office": office}
        )
        found = building_count == 1
        if not found:
            print(
                "No department found with that office building and number.  Try again."
            )
            continue

        found = False
        description = input("Department description--> ")
        description_count: int = collection.count_documents(
            {"description": description}
        )
        found = description_count == 1
        if not found:
            print("No department found with that description.  Try again.")
            continue

    found_department = collection.find_one(
        {
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description,
        }
    )
    return found_department


def delete_department(db):
    department = select_department(db)
    departments = db["departments"]
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    departments = db["departments"].find({}).sort([("abbreviation", pymongo.ASCENDING)])
    for department in departments:
        pprint(department)


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
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    # ************************** Set up the students collection
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

    pprint(departments.index_information())
    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)
