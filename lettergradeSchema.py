import pymongo
from pymongo import MongoClient
def create_letter_grades_collection(db):
  letter_grades: Collection = db["letter_grades"]
  letter_grade_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'An LetterGrade enrollment of a student in a section.',
        'required': [
          'enrollment_id',
          'min_satisfactory'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'enrollment_id': {
            'bsonType': 'integer',
            'description': 'The ID number of the enrollment'
          },
          'min_satisfactory': {
            'bsonType': 'string',
            'enum': {'A','B','C','D','F'},
            'description': 'The minimum satisfactory grade the student must achieve in the course'
          }
        }
      }
    }
  }
  db.create_collection("letter_grades", validator=letter_grade_validator)
