import mysql.connector
from pprint import pprint

from model import SimpleTransaction

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
  return db_write(sql_statement, sql_data)

def remove_user(user_id: str) -> bool:
  sql_statement = """
    DELETE FROM users
    WHERE id = %s
  """
  sql_data = (user_id, )
  return db_write(sql_statement, sql_data)

def save_access_token(user_id, access_token, item_id) -> bool:
  sql_statement = """
    INSERT INTO items (id, user_id, access_token)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE user_id = %s, access_token = %s
  """
  sql_data = (item_id, user_id, access_token, user_id, access_token)
  return db_write(sql_statement, sql_data)

def save_account(account_id, user_id, account_name, account_number) -> bool:
  sql_statement = """
    INSERT INTO accounts (id, user_id, name, number)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE user_id = %s, name = %s, number = %s
  """
  sql_data = (account_id, user_id, account_name, account_number, user_id, account_name, account_number)
  return db_write(sql_statement, sql_data)

def get_accounts(user_id) -> list:
  sql_statement = """
    SELECT * FROM accounts
    WHERE user_id = %s
  """
  sql_data = (user_id, )
  return db_read(sql_statement, sql_data)

def remove_account(account_id: str) -> bool:
  sql_statement = """
    DELETE FROM accounts
    WHERE id = %s
  """
  sql_data = (account_id, )
  return db_write(sql_statement, sql_data)

def add_new_transaction(transaction: SimpleTransaction):
  print("ADDING {}".format(transaction.id))
  pprint(vars(transaction))
  # TODO: need account ID or user ID.
  # TODO: maybe handle duplicate insertions.
  sql_statement = """
    INSERT INTO transactions
      (id, account_id, date, name, amount)
    VALUES (%s, %s, %s, %s, %s)
  """
  sql_data = (transaction.id, transaction.account_id, transaction.date, transaction.name or "", transaction.amount)

  if transaction.pending_transaction_id:
    # TODO: might be a good time to copy over user-related values from
    # that other transaction to this one.
    print("pending transaction")

  return db_write(sql_statement, sql_data)

def delete_transaction(transaction: SimpleTransaction):
  print("REMOVING {}".format(transaction.id))
  sql_statement = """
    DELETE from transactions WHERE id = %s
  """
  sql_data = (transaction.id, )
  return db_write(sql_statement, sql_data)


def get_plaid_items(user_id) -> list:
  sql_statement = """
    SELECT id, access_token, transaction_cursor from items
    WHERE user_id = %s
  """
  sql_data = (user_id, )
  return db_read(sql_statement, sql_data)

# Returns boolean indicating success/failure.
def db_write(statement, data) -> bool:
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    cursor.execute(statement, data)
    # cursor.fetchall() # Necessary?
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
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()

# Returns list of data as list of json (dict).
def db_read(statement, data) -> list:
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    cursor.execute(statement, data)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    row_headers = [x[0] for x in cursor.description]
    json_data = list(map(lambda x: dict(zip(row_headers, x)), rows))

    return json_data

  except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access to DB denied")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
      print("Bad DB")
    else:
      print(err)
    return []
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()

# TODO: Try this consolidated approach (eliminates duplication)
def db_query(read_function, write_function) -> list or bool:
  if not read_function or not write_function: return
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    if read_function: return read_function(cursor, connection)
    else: return write_function(cursor, connection)

  except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access to DB denied")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
      print("Bad DB")
    else:
      print(err)
    return None
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()