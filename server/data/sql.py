import mysql.connector
from typing import Optional

mysql_config = {
    'user': 'money-user',
    'password': 'money-password',
    'host': 'localhost',
    'database': 'money',
    'raise_on_warnings': True
}

def db_write(statement, data):
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(statement, data)
        connection.commit()

# Returns list of data as list of json (dict).
def db_read_list(statement, data = ()) -> list[dict]:
    json_data = []
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(statement, data)
        rows = cursor.fetchall()

        row_headers = [x[0] for x in cursor.description]
        json_data = list(map(lambda x: dict(zip(row_headers, x)), rows))
    return json_data

def db_read_value(statement, data) -> Optional[int | str]:
    value = None
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(statement, data)
        result = cursor.fetchone()
        value = result[0]
    return value

def db_connection():
    try:
        connection = mysql.connector.connect(**mysql_config)
        return connection
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access to DB denied")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Bad DB")
        else:
            print(err)
        return None
