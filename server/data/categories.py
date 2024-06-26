from data.sql import db_read_list, db_read_value, db_write
from model import Category

from mysql.connector.errors import IntegrityError

# TODO: test this.
def init_categories(user_id: str):
    # Ensure that this only happens once per user.
    if db_read_list("SELECT COUNT(*) FROM categories WHERE user_id = %s", (user_id, )):
        print("WARNING: presumed duplicate request to initialize categories for user {}".format(user_id))
        return
    sql_statement = """
        INSERT INTO categories (user_id, parent_id, name)
        SELECT %s, parent_id, name
        FROM categories
        WHERE user_id IS NULL
    """
    sql_data = (user_id)
    try:
        db_write(sql_statement, sql_data)
    except IntegrityError:
        print("Error initializing categories for user {}".format(user_id))

def save_category(user_id, name):
    # This seems to be the best method to "upsert": simple, efficient, doesn't ignore other errors.
    statement = """
        INSERT INTO categories (user_id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = name;
    """
    data = (user_id, name)
    try:
        db_write(statement, data)
    except IntegrityError:
        print("WARNING: error saving category name {} for user {}".format(name, user_id))

def get_category_id(user_id: str, name: str) -> int:
    statement = """
        SELECT id FROM categories WHERE user_id = %s AND name = %s;
    """
    data = (user_id, name)
    try:
        return db_read_value(statement, data)
    except IntegrityError:
        print("WARNING: error looking up category name {} for user {}".format(name, user_id))
        return -1

def update_category(id, name):
    sql_statement = """
        UPDATE categories
        SET name = %s
        WHERE id = %s
    """
    sql_data = (name, id, )
    db_write(sql_statement, sql_data)

def delete_category(id):
    sql_statement = """
        DELETE FROM categories
        WHERE id = %s
    """
    sql_data = (id, )
    db_write(sql_statement, sql_data)

def list_categories(user_id: str) -> list[Category]:
    sql_statement = """
        SELECT * FROM categories
        WHERE user_id = %s
    """
    sql_data = (user_id, )
    rows = db_read_list(sql_statement, sql_data)
    return list(map(lambda x: Category.fromSQLCategory(x), rows))
