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

def save_user(user_id, identifier, display_name):
    sql_statement = """
        INSERT INTO users (id, identifier, display_name)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE identifier = %s, display_name = %s
    """
    sql_data = (user_id, identifier, display_name, identifier, display_name)
    db_write(sql_statement, sql_data)

def delete_user(user_id: str):
    sql_statement = """
        DELETE FROM users
        WHERE id = %s
    """
    sql_data = (user_id, )
    db_write(sql_statement, sql_data)

def save_access_token(user_id, access_token, item_id):
    sql_statement = """
        INSERT INTO items (id, user_id, access_token)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE user_id = %s, access_token = %s
    """
    sql_data = (item_id, user_id, access_token, user_id, access_token)
    db_write(sql_statement, sql_data)

def save_account(account_id, user_id, account_name, account_number):
    sql_statement = """
        INSERT INTO accounts (id, user_id, name, number)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE user_id = %s, name = %s, number = %s
    """
    sql_data = (account_id, user_id, account_name, account_number, user_id, account_name, account_number)
    db_write(sql_statement, sql_data)

def get_accounts(user_id) -> list:
    sql_statement = """
        SELECT * FROM accounts
        WHERE user_id = %s
    """
    sql_data = (user_id, )
    return db_read_list(sql_statement, sql_data)

def delete_account(account_id: str):
    sql_statement = """
        DELETE FROM accounts
        WHERE id = %s
    """
    sql_data = (account_id, )
    db_write(sql_statement, sql_data)

def get_transaction(id: str) -> Optional[SimpleTransaction]:
    sql_statement = """
        SELECT id, account_id, date, name, amount, notes
        FROM transactions
        WHERE id = %s
    """
    sql_data = (id, )
    rows = db_read_list(sql_statement, sql_data)
    if len(rows) != 1: return None
    return SimpleTransaction.fromSQLTransaction(rows[0])

def transaction_sql_statement_base(query: str) -> str:
    sql_statement = """
        FROM transactions
        WHERE user_id = %(id)s
    """
    if query:
        # TODO: make search more robust by splitting the query terms. e.g. "a b" should match "b c a".
        # For each field f and words a and b we need: (f like a and f like b)
        sql_statement += """
            AND (
                name LIKE %(query)s OR
                amount LIKE %(query)s OR
                notes LIKE %(query)s
            )
        """
    return sql_statement

def get_transaction_count(user_id: str,
                          query: Optional[str] = None) -> int:
    sql_statement = "SELECT COUNT(*)"
    sql_statement += transaction_sql_statement_base(query)
    sql_data = {
        'id': user_id,
        'query': '%{}%'.format(query)
    }
    return db_read_value(sql_statement, sql_data)

# The offset specifies the offset of the first row to return. The offset of the first row is 0, not 1.
# The row_count specifies the maximum number of rows to return.
# The query is an optional string of search terms.
def get_transactions(user_id: str,
                     offset: int = 0,
                     row_count: int = 10,
                     query: Optional[str] = None) -> list[SimpleTransaction]:
    sql_statement = "SELECT id, account_id, date, name, amount, notes"
    sql_statement += transaction_sql_statement_base(query)
    sql_statement += """
        ORDER BY date DESC
        LIMIT %(offset)s, %(row_count)s
    """
    sql_data = {
        'id': user_id,
        'query': '%{}%'.format(query),
        'offset': offset,
        'row_count': row_count
    }
    rows = db_read_list(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def get_transactions_for_account(account_id: str) -> list[SimpleTransaction]:
    sql_statement = """
        SELECT id, account_id, date, name, amount
        FROM transactions
        WHERE account_id = %s
    """
    sql_data = (account_id, )
    rows = db_read_list(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def add_transaction(transaction: SimpleTransaction):
    # print("ADDING {}".format(transaction.id))
    # pprint(vars(transaction))
    # TODO: maybe handle duplicate insertions.
    sql_statement = """
        INSERT INTO transactions
            (id, user_id, account_id, date, name, amount, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    sql_data = (transaction.id, transaction.user_id, transaction.account_id, transaction.date, transaction.name or "", transaction.amount, transaction.note or "")

    if transaction.pending_transaction_id:
        # TODO: might be a good time to copy over user-related values from
        # that other transaction to this one.
        print("WARNING: pending transaction")

    db_write(sql_statement, sql_data)

def modify_transaction(transaction: SimpleTransaction):
    sql_statement = """
        UPDATE transactions
        SET
        account_id = IFNULL(%s, account_id),
        date = IFNULL(%s, date),
        name = IFNULL(%s, name),
        amount = IFNULL(%s, amount),
        notes = IFNULL(%s, notes)
        WHERE id = %s
    """
    sql_data = (
        transaction.account_id,
        transaction.date,
        transaction.name,
        transaction.amount,
        transaction.note,
        transaction.id
    )
    db_write(sql_statement, sql_data)

def delete_transaction(transaction_id: str):
    print("REMOVING {}".format(transaction_id))
    # Consider marking removed instead of deleting, but you'd need to rename the ID
    # (e.g. transactionId + "-REMOVED-" + random UUID) to avoid future collisions
    sql_statement = """
        DELETE FROM transactions WHERE id = %s
    """
    sql_data = (transaction_id, )
    db_write(sql_statement, sql_data)

def get_plaid_items(user_id) -> list[dict]:
    sql_statement = """
        SELECT id, access_token, transaction_cursor
        FROM items
        WHERE user_id = %s
    """
    sql_data = (user_id, )
    return db_read_list(sql_statement, sql_data)

def save_transaction_cursor(item_id: str, cursor: str):
    sql_statement = """
        UPDATE items
        SET transaction_cursor = %s
        WHERE id = %s
    """
    sql_data = (cursor, item_id)
    db_write(sql_statement, sql_data)

# Returns boolean indicating success/failure.
def db_write(statement, data):
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(statement, data)
        connection.commit()

# Returns list of data as list of json (dict).
def db_read_list(statement, data) -> list[dict]:
    json_data = []
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(statement, data)
        rows = cursor.fetchall()

        row_headers = [x[0] for x in cursor.description]
        json_data = list(map(lambda x: dict(zip(row_headers, x)), rows))
    return json_data

def db_read_value(statement, data) -> Optional[int or str]:
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
