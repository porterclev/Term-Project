import pymongo
from pymongo import MongoClient
def create_courses_collection(db):
  courses: Collection = db["courses"]
  course_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'A course offered by a specific department',
        'required': [
          'department_abbreviation',
          'course_number',
          'name',
          'description',
          'units'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'department_abbreviation': {
            'bsonType': 'string',
            'maxLength': 6,
            'description': 'The abbreviation of the department that offers the course.'
          },
          'course_number': {
            'bsonType': 'integer',
            'description': 'The number of the course within the department.'
          },
          'name': {
            'bsonType': 'string',
            'maxLength': 50,
            'description': 'The name of the course.'
          },
          'description': {
            'bsonType': 'string',
            'maxLength': 80,
            'description': 'Text about the course.'
          },
          'units': {
            'bsonType': 'integer',
            'description': 'The number of units the course is worth.'
          }
        }
      }
    }
  }
  db.create_collection("courses", validator=course_validator)
