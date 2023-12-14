def create_majors_collection(db):
  majors: Collection = db["majors"]
  major_validator = 
  {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'description': 'An enrollment of a student into a section.',
        'required': [
          'name',
          'description'
        ],
        'additionalProperties': False,
        'properties': {
          '_id': {},
          'name': {
            'bsonType': 'string',
            'description': 'The name of the major'
          },
          'description': {
            'bsonType': 'string',
            'description': 'Text about the major'
          }
        }
      }
    }
  }
  db.create_collection["majors", validator=major_validator)
