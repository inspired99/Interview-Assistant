def register_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO Users (user_id) VALUES({user_id});")
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
        cursor.execute(("SELECT * FROM (SELECT * FROM ("
                        "Tasks "
                        "LEFT JOIN ("
                        f"SELECT * FROM Solved WHERE user_id = {user_id}"
                        ") AS S ON (Tasks.id = S.task_id)) "
                        "WHERE (S.task_id IS NULL)) AS A "
                        f"JOIN (SELECT company FROM UsersCompanies WHERE (user_id = {user_id})) "
                        "AS B ON (A.company = B.company) "
                        f"JOIN (SELECT stage FROM UsersStages WHERE (user_id = {user_id})) "
                        "AS C ON (A.stage = C.stage);"))
    data = cursor.fetchall()
    cursor.close()
    return data


def insert_element(conn, table_name, user_id, attribute, element):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (user_id, {attribute}) VALUES({user_id}, '{element}');")
    conn.commit()
    cursor.close()


def delete_element(conn, table_name, user_id, attribute, element):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE (user_id = {user_id} AND {attribute} = '{element}');")
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
