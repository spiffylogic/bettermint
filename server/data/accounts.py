from data.sql import db_read_list, db_write

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
