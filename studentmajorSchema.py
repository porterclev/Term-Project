import pymongo
from pymongo import MongoClient
def create_student_majors_collection(db):
  student_majors: Collection = db["student_majors"]
  student_major_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'An instance of a student in a particular major.',
        'required': [
          'student_id',
          'major_name',
          'declaration_date'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'student_id': {
            'bsonType': 'integer',
            'description': 'The ID number of the student'
          },
          'section_id': {
            'bsonType': 'string',
            'description': 'The ID number of the section the student is enrolling in'
          },
          'declaration_date'
            'bsonType': 'date',
            'description': 'The date the student declared the major'
          }
        }
      }
    }
  }
  db.create_collection("student_majors", validator=student_major_validator)
