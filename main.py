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

if __name__ == "__main__":
    config = ConfigParser()
    config.sections()
    config.read("config.config")
    print(config["Mongo"]["USERNAME"])
    username = config["Mongo"]["USERNAME"]
    password = config["Mongo"]["PASSWORD"]
    project = config["Mongo"]["PROJECT"]
    hash_name = config["Mongo"]["HASH"]
    database_name = input("database name (press ENTER for 'Demonstration')-->") or "Demonstration"#just press enter :/
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
    main_action: str = ""
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print("next action: ", main_action)
        exec(main_action)


