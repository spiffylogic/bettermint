import mysql.connector
from pprint import pprint
from typing import *

from model import SimpleTransaction

mysql_config = {
    'user': 'money-user',
    'password': 'money-password',
    'host': 'localhost',
    'database': 'money',
    'raise_on_warnings': True
}

def save_user(user_id, identifier, display_name) -> bool:
    sql_statement = """
        INSERT INTO users (id, identifier, display_name)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE identifier = %s, display_name = %s
    """
    sql_data = (user_id, identifier, display_name, identifier, display_name)
    return db_write(sql_statement, sql_data)

def delete_user(user_id: str) -> bool:
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

def delete_account(account_id: str) -> bool:
    sql_statement = """
        DELETE FROM accounts
        WHERE id = %s
    """
    sql_data = (account_id, )
    return db_write(sql_statement, sql_data)

def get_transaction(id: str) -> Optional[SimpleTransaction]:
    sql_statement = """
        SELECT id, account_id, date, name, amount
        FROM transactions
        WHERE id = %s
    """
    sql_data = (id, )
    rows = db_read(sql_statement, sql_data)
    if len(rows) != 1: return None
    return SimpleTransaction.fromSQLTransaction(rows[0])

# The offset specifies the offset of the first row to return. The offset of the first row is 0, not 1.
# The row_count specifies the maximum number of rows to return.
def get_transactions_for_user(user_id: str, offset: int = 0, row_count: int = 10) -> list[SimpleTransaction]:
    sql_statement = """
        SELECT t.id, t.account_id, t.date, t.name, t.amount
        FROM transactions AS t
        INNER JOIN accounts AS a
        ON t.account_id = a.id
        WHERE a.user_id = %s
        LIMIT %s, %s
    """
    sql_data = (user_id, offset, row_count)
    rows = db_read(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def get_transactions_for_account(account_id: str) -> list[SimpleTransaction]:
    sql_statement = """
        SELECT id, account_id, date, name, amount
        FROM transactions
        WHERE account_id = %s
    """
    sql_data = (account_id, )
    rows = db_read(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def add_transaction(transaction: SimpleTransaction):
    # print("ADDING {}".format(transaction.id))
    # pprint(vars(transaction))
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

def modify_transaction(transaction: SimpleTransaction):
    sql_statement = """
        UPDATE transactions
        SET account_id = %s, date = %s, name = %s, amount = %s
        WHERE id = %s
    """
    sql_data = (transaction.account_id, transaction.date, transaction.name or "", transaction.amount, transaction.id)
    return db_write(sql_statement, sql_data)

def delete_transaction(transaction_id: str) -> bool:
    print("REMOVING {}".format(transaction_id))
    # Consider marking removed instead of deleting, but you'd need to rename the ID
    # (e.g. transactionId + "-REMOVED-" + random UUID) to avoid future collisions
    sql_statement = """
        DELETE FROM transactions WHERE id = %s
    """
    sql_data = (transaction_id, )
    return db_write(sql_statement, sql_data)

def get_plaid_items(user_id) -> list[dict]:
    sql_statement = """
        SELECT id, access_token, transaction_cursor
        FROM items
        WHERE user_id = %s
    """
    sql_data = (user_id, )
    return db_read(sql_statement, sql_data)

def save_transaction_cursor(item_id: str, cursor: str):
    sql_statement = """
        UPDATE items
        SET transaction_cursor = %s
        WHERE id = %s
    """
    sql_data = (cursor, item_id)
    return db_write(sql_statement, sql_data)

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
def db_read(statement, data) -> list[dict]:
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
