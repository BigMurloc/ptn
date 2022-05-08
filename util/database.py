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
    cursor.execute("DROP TABLE IF EXISTS topic")

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
        "password TEXT NOT NULL, "
        "active_topic TEXT, "
        "FOREIGN KEY (owner) REFERENCES users(id), "
        "FOREIGN KEY (active_topic) REFERENCES topic(name) "
        ") "
    )

    cursor.execute(
        "CREATE TABLE topic ( "
        "id INTEGER PRIMARY KEY, "
        "room_id INTEGER REFERENCES room(id), "
        "name TEXT, "
        "description TEXT, "
        "score INTEGER DEFAULT 0, "
        "UNIQUE(room_id, name) "
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
