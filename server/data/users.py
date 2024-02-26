from data.sql import db_write, db_read_list

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

def get_plaid_items(user_id) -> list[dict]:
    sql_statement = """
        SELECT id, access_token, transaction_cursor
        FROM items
        WHERE user_id = %s
    """
    sql_data = (user_id, )
    return db_read_list(sql_statement, sql_data)
