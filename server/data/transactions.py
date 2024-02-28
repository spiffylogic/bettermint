from data.sql import db_read_list, db_read_value, db_write
from model import SimpleTransaction
from typing import Optional

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
    # TODO: handle duplicate insertions.
    # Example error on write:
    # mysql.connector.errors.IntegrityError: 1062 (23000): Duplicate entry 'Qna3gxg1r8ugxzNPdoGjcMm5X9aGJnsjlq7eW' for key 'transactions.PRIMARY'
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

def save_transaction_cursor(item_id: str, cursor: str):
    sql_statement = """
        UPDATE items
        SET transaction_cursor = %s
        WHERE id = %s
    """
    sql_data = (cursor, item_id)
    db_write(sql_statement, sql_data)
