import sqlite3
from jinjasql import JinjaSql

j = JinjaSql(param_style='pyformat')


def connect_discord(db):
    try:
        conn = sqlite3.connect(db)
        print('Connection successful!')
        return conn
    except:
        print('Could not connect to the database.')


def create_table(conn, sql_create_table_command):
    # Pass sqlite db connection and sql statement to create a new table
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table_command)
    except:
        print('Could not create table. Check syntax.')


def write_to_table(conn, sql_write_table):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_write_table)
        print(cursor.lastrowid)  # > 0 means it worked
        conn.commit()

    except:
        print('Could not write to table. Check syntax and if table exists.')


def sqlite_insert(conn, table, row):
    # programmatically generate sql insert command
    # isolate column headers and values from row input
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())

    # use cols and vals to generate sql insert string, tailored to specific SQL table. Maybe could change to switch/case
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    print('SQL Insert successful.')

    # commit table insert to database
    conn.cursor().execute(sql, row)
    conn.commit()
    return

