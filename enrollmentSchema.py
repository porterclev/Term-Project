import pymongo
from pymongo import MongoClient
def create_enrollments_collection(db):
  enrollments: Collection = db["enrollments"]
  enrollment_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'An enrollment of a student into a section.',
        'required': [
          'student_id',
          'section_id',
          'enrollment_type'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'student_id': {
            'bsonType': 'integer',
            'description': 'The ID number of the student enrolling'
          },
          'section_id': {
            'bsonType': 'integer',
            'description': 'The ID number of the section the student is enrolling in'
          },
          'enrollment_type': {
            'bsonType': 'string',
            'enum': ['PassFail', 'LetterGrade'],
            'description': 'The type of enrollment the student has in the section'
          }
        }
      }
    }
  }
  db.create_collection("enrollments", validator=enrollment_validator)
