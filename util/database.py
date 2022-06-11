import sqlite3
from os.path import exists
from sqlite3 import Connection

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.util._compat_py3k import asynccontextmanager

Base = declarative_base()
engine = create_async_engine(
            "sqlite+aiosqlite:///resources/roomies.db",
            echo=True,
            future=True
        )

@asynccontextmanager
async def get_database_orm() -> AsyncSession:

    global engine

    if engine is None:
        engine = create_async_engine(
            "sqlite+aiosqlite://resources/roomies.db",
            echo=True,
            future=True
        )
    async with sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
    )() as session:
        yield session


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
    cursor.execute("DROP TABLE IF EXISTS vote")

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
        "name TEXT NOT NULL, "
        "password TEXT NOT NULL, "
        "active_topic INTEGER, "
        "FOREIGN KEY (owner) REFERENCES users(id), "
        "FOREIGN KEY (active_topic) REFERENCES topic(id) "
        ") "
    )

    cursor.execute(
        "CREATE TABLE topic ( "
        "id INTEGER PRIMARY KEY, "
        "room_id INTEGER REFERENCES room(id), "
        "name TEXT, "
        "description TEXT, "
        "UNIQUE(room_id) "
        ") "
    )

    cursor.execute(
        "CREATE TABLE participant ( "
        "id INTEGER PRIMARY KEY, "
        "user_id INTEGER NOT NULL, "
        "room_id INTEGER NOT NULL, "
        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, "
        "FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE, "
        "UNIQUE (user_id, room_id) "
        ") "
    )

    cursor.execute(
        "CREATE TABLE vote ( "
        "user_id INTEGER NOT NULL, "
        "topic_id INTEGER NOT NULL, "
        "vote INTEGER NOT NULL CHECK ( vote IN (-2, -1, 0, 0.5, 1, 2, 3, 5, 8, 13, 20, 50, 100, 200) ), "
        "PRIMARY KEY (user_id, topic_id), "
        "FOREIGN KEY (user_id) REFERENCES users(id), "
        "FOREIGN KEY (topic_id) REFERENCES topic(id) "
        ") "
    )

    connection.commit()
