import mysql.connector

mysql_config = {
  'user': 'money-user',
  'password': 'money-password',
  'host': 'localhost',
  'database': 'money',
  'raise_on_warnings': True
}

def upsert_user(user_id, identifier, display_name) -> bool:
  sql_statement = """
    INSERT INTO users (id, identifier, display_name)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE identifier = %s, display_name = %s
  """
  sql_data = (user_id, identifier, display_name, identifier, display_name)
  return run_sql(sql_statement, sql_data)

def save_access_token(user_id, access_token, item_id) -> bool:
  sql_statement = """
    INSERT INTO plaid (user_id, access_token, item_id)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE access_token = %s, item_id = %s
  """
  sql_data = (user_id, access_token, item_id, access_token, item_id)
  return run_sql(sql_statement, sql_data)

def save_account(user_id, account_name, account_number) -> bool:
  sql_statement = """
    INSERT INTO accounts (user_id, name, number)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE name = %s, number = %s
  """
  sql_data = (user_id, account_name, account_number, account_name, account_number)
  return run_sql(sql_statement, sql_data)

def get_accounts(user_id) -> list:
  sql_statement = """
    SELECT * from accounts
    WHERE user_id = %s
  """
  sql_data = (user_id, )
  return run_sql_fetch(sql_statement, sql_data)

def run_sql(statement, data) -> bool:
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    cursor.execute(statement, data)
    cursor.fetchall()
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

def run_sql_fetch(statement, data) -> list:
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    cursor.execute(statement, data)

    rows = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    json_data = list(map(lambda x: dict(zip(row_headers, x)), rows))

    connection.commit()
    cursor.close()
    connection.close()

    return json_data
  except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access to DB denied")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
      print("Bad DB")
    else:
      print(err)
  return []
