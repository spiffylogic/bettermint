from data.sql import db_read_list, db_write
from model import Category

from mysql.connector.errors import IntegrityError

def create_category(name: str):
    sql_statement = """
        INSERT INTO categories (name)
        VALUES (%s)
    """
    sql_data = (name, )
    try:
        db_write(sql_statement, sql_data)
    except IntegrityError:
        print("WARNING: ignoring duplicate category name {}".format(name))

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

def list_categories() -> list[Category]:
    sql_statement = """
        SELECT * FROM categories
    """
    rows = db_read_list(sql_statement)
    return list(map(lambda x: Category.fromSQLCategory(x), rows))
