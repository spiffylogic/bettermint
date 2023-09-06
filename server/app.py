from flask import abort, request, Flask
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

config = {
  'user': 'money-user',
  'password': 'money-password',
  'host': 'localhost',
  'database': 'money',
  'raise_on_warnings': True
}

@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
  if request.method == 'GET':
    # TODO: return the information for <user_id>
    return '{{}}'
  if request.method == 'POST':
    # modify/update the information for <user_id>
    # data = request.form # a multidict containing POST data
    if not upsert(user_id, request.json['identifier'], request.json['display_name']):
      abort(500) # Something went wrong
    return '{{}}'
  if request.method == 'DELETE':
    # TODO: delete user with ID <user_id>
    return '{{}}'
  else:
    # POST Error 405 Method Not Allowed
    abort(405)

def upsert(user_id, identifier, display_name) -> bool:
  try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    sql_statement = ("REPLACE INTO users "
                  "(uid, identifier, display_name) "
                  "VALUES (%s, %s, %s)")
    sql_data = (user_id, identifier, display_name)
    cursor.execute(sql_statement, sql_data)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access to DB denied")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
      print("Bad DB")
    else:
      print(err)
  return False
