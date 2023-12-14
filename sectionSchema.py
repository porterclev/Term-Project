import pymongo
from pymongo import MongoClient
def create_sections_collection(db):
  sections: Collection = db["sections"]
  section_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'A section of a particular course',
        'required': [
          'department_abbreviation',
          'course_number',
          'section_number',
          'semester',
          'section_year',
          'building',
          'room',
          'schedule',
          'start_time',
          'instructor'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'department_abbreviation': {
            'bsonType': 'string',
            'maxLength': 10,
            'description': 'The abbreviation of the department that offers the course the section is of.'
          },
          'course_number': {
            'bsonType': 'integer',
            'description': 'The course number for the course the section is of.'
          },
          'section_number': {
            'bsonType': 'integer',
            'description': 'The number of the specific section.'
          },
          'semester': {
            'bsonType': 'string',
            'enum': ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II'],
            'maxLength': 10,
            'description': 'The semester the section takes place during.'
          },
          'section_year': {
            'bsonType': 'integer',
            'description': 'The year the section takes place during.'
          },
          'building': {
            'bsonType': 'string',
            'enum': [
              'ANAC', 'CDC', 'DC',
              'ECS',  'EN2', 'EN3',
              'EN4',  'EN5', 'ET',
              'HSCI', 'NUR', 'VEC'
            ],
            'maxLength': 6,
            'description': 'The building the section takes place in.'
          },
          'room': {
            'bsonType': 'integer',
            'minValue' = 1,
            'maxValue' = 999,
            'description': 'The number of the room the section takes place in.'
          },
          'schedule': {
            'bsonType': 'string',
            'maxLength': 6,
            'enum': ['MW', 'TuTh', 'MWF', 'F', 'S'],
            'description': 'The days of the week on which the section takes place.'
          },
          'start_time': {
            'bsonType': 'time',
            'description': 'The time of day at which the section begins.'
          },
          'instructor': {
            'bsonType': 'string',
            'maxLength': 80,
            'description': 'The instructor teaching the section.'
          }
        }
      }
    }
  }
  db.create_collection("sections", validator=section_validator)       
