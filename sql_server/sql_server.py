# import pymysql
# from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT
#
#
# conn = pymysql.connect(database=USER_NAME, user=DATABASE_NAME, password=PASSWORD, host=HOST_NAME, port=PORT)

import psycopg2
from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT


def register_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO Users (user_id, companies) VALUES({user_id}, ARRAY['', '', '', '', '', '', '', '']);")
    conn.commit()
    cursor.close()


def read_table(conn, table_name, flag_take_task=None, user_id=None, task_id=None):
    cursor = conn.cursor()
    if flag_take_task is None:
        if task_id is None:  # Search in Users, Current
            condition = f"user_id = {user_id}"
        elif user_id is None:  # Search in Tasks
            condition = f"id = {task_id}"
        else:
            condition = f"user_id = {user_id} AND task_id = {task_id}"

        cursor.execute(f"SELECT * FROM {table_name} WHERE ({condition});")
    else:
        cursor.execute(("SELECT * FROM "
                        "(SELECT * FROM"
                        "(Tasks LEFT JOIN "
                        f"(SELECT * FROM Solved WHERE user_id = {user_id})"
                        "AS R ON (Tasks.id = R.task_id)) WHERE R.task_id IS NULL)"
                        "AS T ORDER BY RANDOM() LIMIT 1;"))
    data = cursor.fetchall()
    cursor.close()
    return data


def insert_company(conn, user_id, company_index, company_name):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Users SET companies[{company_index + 1}] = '{company_name}' WHERE user_id = '{user_id}';")
    conn.commit()
    cursor.close()


def delete_company(conn, user_id, company_index):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Users SET companies[{company_index + 1}] = '' WHERE user_id = '{user_id}';")
    conn.commit()
    cursor.close()


def insert_task(conn, table_name, user_id, task_id):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (task_id, user_id) VALUES({task_id}, {user_id});")
    conn.commit()
    cursor.close()


def remove_task(conn, table_name, user_id, task_id):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE (task_id = {task_id} AND user_id = {user_id});")
    conn.commit()
    cursor.close()
