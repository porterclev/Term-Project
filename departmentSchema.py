def create_departments_collection(db):
  departments: Collection = db["departments"]
  department_validator = 
    {
      'validator': {
        '$jsonSchema': {
          'bsonType': 'object',
          'description': 'A department in the university',
          'required': [
            'name',
            'abbreviation',
            'chair_name',
            'building',
            'office',
            'description'
          ],
          'additionalProperties': false,
          'properties': {
            '_id': {},
            'name': {
              'bsonType': 'string',
              'minLength': 10,
              'maxLength': 50,
              'description': 'The name of the department'
            },
            'abbreviation': {
              'bsonType': 'string',
              'maxLength': 6,
              'description': 'An abbreviation of the department'
            },
            'chair_name': {
              'bsonType': 'string',
              'maxLength': 80,
              'description': 'the name of the head of the department'
            },
            'building': {
              'enum': [
                'ANAC', 'CDC', 'DC',
                'ECS',  'EN2', 'EN3',
                'EN4',  'EN5', 'ET',
                'HSCI', 'NUR', 'VEC'
              ],
              'description': 'An abbreviation of the department'
            },
            'office': { 
              'bsonType': 'number', 
              'description': 'office number' 
            },
            'description': {
              'bsonType': 'string',
              'minLength': 10,
              'maxLength': 80,
              'description': 'text about the department'
            }
          }
        }
      }
    }
    db.create_collection("departments", validator=department_validator)

$comment:'run lines bellow in shell'
department_validator =  {'validator': {'$jsonSchema': {'bsonType': "object",'description': 'A department in the university','required': ['name', 'abbreviation', 'chair_name','building','office','description'],'additionalProperties': false,'properties': {'_id': {},'name': {'bsonType':'string','minLength':10,'maxLength':50,'description':'The name of the department'},'abbreviation': {'bsonType':'string','maxLength':6,'description':'An abbreviation of the department'},'chair_name': {'bsonType':'string','maxLength':80,'description':'the name of the head of the department'},'building': {'bsonType':'string','enum':['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3','EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],'description':'An abbreviation of the department'},'office': {'bsonType':"number",'description':'office number'},'description': {'bsonType':'string','minLength': 10,'maxLength':80,'description':'text about the department'}}}} }
db.createCollection('departments', department_validator)

d1 = {'name':'Porters department', 'abbreviation':'PD', 'chair_name':'Porter', 'building':'CDC','office':1,'description':'porters department'}
db['departments'].insertOne(d1)
d2 = {'name':'Andrews department', 'abbreviation':'AD', 'chair_name':'Andrew', 'building':'VEC','office':1,'description':'andrews department'}
db['departments'].insertOne(d2)


$comment: this will error because the building isn't in enum 
d3 = {'name':'Emilys department', 'abbreviation':'ED', 'chair_name':'Emily', 'building':'bruh','office':1,'description':'Emilys department'}
db['departments'].insertOne(d3)

