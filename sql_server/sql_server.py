# import pymysql
# from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT
#
#
# conn = pymysql.connect(database=USER_NAME, user=DATABASE_NAME, password=PASSWORD, host=HOST_NAME, port=PORT)

import psycopg2
from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT
conn = psycopg2.connect(
    host=HOST_NAME,
    database=DATABASE_NAME,
    user=USER_NAME,
    password=PASSWORD,
    port=PORT)


def create_table(table_name):
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, name VARCHAR)")
    conn.commit()
    cursor.close()


def insert():
    cursor = conn.cursor()
    сursor.execute(f"INSERT INTO {table_name} (name) VALUES(%s)", ("Cristina",))
    conn.commit()
    cursor.close()


def read(table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student;")
    for row in rows:
        print(row)
    cursor.close()

def delete_table(table_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE {table_name};")


def delete_rows(table_name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parts WHERE part_id = %s", (part_id,))
    conn.commit()
    cursor.close()


create_table("test")

conn.close()

