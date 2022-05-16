import sqlite3
from sqlite3 import Connection, IntegrityError

from user.repository.exceptions import ExistingUser
from user.repository.user_model import User


class UserRepository:

    def __init__(self, db_connection: Connection):
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    def find_all(self):
        self.db_cursor.execute("SELECT * FROM users")

        user_tuples = self.db_cursor.fetchall()
        users = []

        for user_tuple in user_tuples:
            users.append(self.__user_tuple_mapper(user_tuple))

        return users

    def find_by_username(self, username):
        self.db_connection.row_factory = sqlite3.Row
        self.db_cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )

        return self.__user_tuple_mapper(self.db_cursor.fetchone())

    def save(self, username, password):
        try:
            self.db_cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
            )
        except IntegrityError:
            raise ExistingUser

        self.db_connection.commit()

    def delete_by_username(self, username):
        self.db_cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.db_connection.commit()

    def is_username_unique(self, username):
        self.db_cursor.execute("SELECT * FROM users WHERE username = ? ", (username,))
        return self.db_cursor.fetchone() is None

    def __user_tuple_mapper(self, user_tuple):
        return User(user_tuple[0], user_tuple[1], user_tuple[2])
