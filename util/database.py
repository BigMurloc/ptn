import sqlite3
from os.path import exists
from sqlite3 import Connection


def get_database():
    db_path = "resources/roomies.db"

    if not exists(db_path):
        connection = sqlite3.connect(db_path)
        init_db(connection)
        return connection

    return sqlite3.connect(db_path)


def init_db(connection: Connection):
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS room")
    cursor.execute("DROP TABLE IF EXISTS participant")

    connection.commit()

    cursor.execute(
        "CREATE TABLE users ("
        "id INTEGER PRIMARY KEY, "
        "username TEXT NOT NULL UNIQUE, "
        "password TEXT NOT NULL"
        ")"
    )

    cursor.execute(
        "CREATE TABLE room ( "
        "id INTEGER PRIMARY KEY, "
        "owner INTEGER NOT NULL, "
        "password TEXT NOT NULL,"
        "FOREIGN KEY (owner) REFERENCES users(id)"
        ") "
    )

    cursor.execute(
        "CREATE TABLE participant ( "
        "id INTEGER PRIMARY KEY, "
        "user_id INTEGER NOT NULL, "
        "room_id INTEGER NOT NULL, "
        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, "
        "FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE "
        ") "
    )

    connection.commit()
