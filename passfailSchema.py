def create_pass_fail_collection(db):
  pass_fails: Collection = db["pass_fails"]
  pass_fail_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'An PassFail enrollment of a student in a section.',
        'required': [
          'enrollment_id',
          'application_date'
        ],
        'additionalProperties': false,
        'properties': {
          '_id': {},
          'enrollment_id': {
            'bsonType': 'integer',
            'description': 'The ID number of the enrollment'
          },
          'application_date': {
            'bsonType': 'date',
            'description': 'The date of the student application to the section'
          }
        }
      }
    }
  }
  db.create_collection("pass_fails", validator=pass_fail_validator)
