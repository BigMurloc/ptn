from sqlite3 import Connection

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from user.repository.UserDB import UserDB
from user.repository.exceptions import ExistingUser
from util.database import get_database_orm


class UserRepository:

    def __init__(self, db_connection: Connection):
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    async def find_all(self, user_filter):
        if user_filter is None:
            user_filter = ''

        async with get_database_orm() as session:
            return (await session.execute(
                select(UserDB).where(UserDB.username.like(user_filter + '%'))
            )).scalars()

    async def find_by_username(self, username):
        async with get_database_orm() as session:
            return (await session.execute(
                select(UserDB)
                    .where(UserDB.username == username))).scalars().first()

    async def save(self, username, password):
        try:
            async with get_database_orm() as session:
                async with session.begin():
                    user = UserDB(
                        username=username,
                        password=password
                    )
                    session.add(user)

        except IntegrityError:
            raise ExistingUser

    def delete_by_username(self, username):
        self.db_cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.db_connection.commit()

