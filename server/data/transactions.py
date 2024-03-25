from data.categories import get_category_id, save_category
from data.sql import db_read_list, db_read_value, db_write
from model import SimpleTransaction

from mysql.connector.errors import IntegrityError
from pprint import pprint
from typing import Optional

def build_sql_statement(data: dict, count: bool = False):
    fields = "t.id, account_id, date, t.name, amount, notes, category_id, c.name as category_name"
    statement = """
        SELECT {} FROM transactions AS t
        LEFT JOIN categories AS c ON t.category_id = c.id
    """.format("COUNT(*)" if count else fields)

    if 'user_id' in data:
        statement += "WHERE t.user_id = %(user_id)s\n"
    elif 'account_id' in data:
        statement += "WHERE account_id = %(id)s\n"
    elif 'id' in data:
        statement += "WHERE t.id = %(id)s\n"

    if 'query' in data:
        # TODO: make search more robust by splitting the query terms. e.g. "a b" should match "b c a".
        # For each field f and words a and b we need: (f like a and f like b)
        statement += """
            AND (
                name LIKE %(query)s OR
                amount LIKE %(query)s OR
                notes LIKE %(query)s
            )
        """
    statement += "ORDER BY date DESC\n"
    if 'offset' in data and 'row_count' in data:
        statement += "LIMIT %(offset)s, %(row_count)s\n"
    return statement

def get_transaction(id: str) -> Optional[SimpleTransaction]:
    sql_data = { 'id': id }
    sql_statement = build_sql_statement(sql_data)
    rows = db_read_list(sql_statement, sql_data)
    if len(rows) != 1: return None
    return SimpleTransaction.fromSQLTransaction(rows[0])

def get_transaction_count(user_id: str,
                          query: Optional[str] = None) -> int:
    sql_data = {}
    sql_data['user_id'] = user_id
    if query: sql_data['query'] = '%{}%'.format(query)
    sql_statement = build_sql_statement(sql_data, count = True)
    return db_read_value(sql_statement, sql_data)

# The offset specifies the offset of the first row to return. The offset of the first row is 0, not 1.
# The row_count specifies the maximum number of rows to return.
# The query is an optional string of search terms.
def get_transactions(user_id: str,
                     offset: int = 0,
                     row_count: int = 10,
                     query: Optional[str] = None) -> list[SimpleTransaction]:
    sql_data = {
        'user_id': user_id,
        'offset': offset,
        'row_count': row_count
    }
    if query: sql_data['query'] = '%{}%'.format(query)
    sql_statement = build_sql_statement(sql_data)
    rows = db_read_list(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def get_transactions_for_account(account_id: str) -> list[SimpleTransaction]:
    sql_data = { 'account_id': account_id }
    sql_statement = build_sql_statement(sql_data)
    rows = db_read_list(sql_statement, sql_data)
    return list(map(lambda x: SimpleTransaction.fromSQLTransaction(x), rows))

def add_transaction(transaction: SimpleTransaction):
    # Whenever we do this, we could/should upsert the category
    if transaction.category_name:
        save_category(transaction.user_id, transaction.category_name)
        transaction.category_id = get_category_id(transaction.user_id, transaction.category_name)
    sql_statement = """
        INSERT INTO transactions
            (id, user_id, account_id, category_id, date, name, amount, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    sql_data = (transaction.id, transaction.user_id, transaction.account_id, transaction.category_id, transaction.date, transaction.name or "", transaction.amount, transaction.note or "")

    if transaction.pending_transaction_id:
        # TODO: might be a good time to copy over user-related values from
        # that other transaction to this one.
        print("WARNING: {} has pending transaction {}".format(transaction.id, transaction.pending_transaction_id))

    try:
        db_write(sql_statement, sql_data)
    except IntegrityError:
        # TODO: handle duplicate insertions.
        print("WARNING: ignoring duplicate transaction {}".format(transaction.id))
        pprint(vars(transaction))

def modify_transaction(transaction: SimpleTransaction):
    sql_statement = """
        UPDATE transactions
        SET
        account_id = IFNULL(%s, account_id),
        category_id = IFNULL(%s, category_id),
        date = IFNULL(%s, date),
        name = IFNULL(%s, name),
        amount = IFNULL(%s, amount),
        notes = IFNULL(%s, notes)
        WHERE id = %s
    """
    sql_data = (
        transaction.account_id,
        int(transaction.category_id) if transaction.category_id else None,
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
