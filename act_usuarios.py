import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tabla
              SET cedula = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def main():
    database = r'C:\\Users\\Corimon\\OneDrive - Corimon\\CORIMON\\CRP\\ROMANA CRP\\PLATAFORMA\\SERVIDOR_PESAJE\\static\\db\\usuarios.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, ('1111111', 1))


if __name__ == '__main__':
    main()