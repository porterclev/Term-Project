import pymongo
from pymongo import MongoClient
def create_students_collection(db):
  students: Collection = db["students"]
  student_validator={
    'validator': {
      '$jsonSchema': {
        'bsonType': "object",
        'description': 'A person attending university to earn a degree or credential',
        'required': ['last_name', 'first_name','e_mail'],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'last_name': {
            'bsonType': 'string',
            'description': 'surname of the student',
            'minLength': 3,
            'maxLength': 80
            },
            'first_name': {
            'bsonType': 'string',
            'description': 'given name of the student',
            'minLength': 3,
            'maxLength': 80
            },
            'e_mail': {
              'bsonType': 'string',
              'description': 'electronic mail address of the student',
              'minLength': 10,
              'maxLength': 255
            }
          }
        }
      }
    }
    db.create_collection("students", validator=student_validator)
