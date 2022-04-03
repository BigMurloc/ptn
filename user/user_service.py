from getpass import getpass

import bcrypt

from repository.repository import Repository
from user.user_state import UserState


class UserService:

    def login(self, username):
        user = Repository().find_by_username(username)
        raw_password = getpass()
        if self.verify_password(raw_password, user.password):
            print('Login success!')
            UserState().is_logged_in = True
        else:
            print('Login failure')

    def list_all(self, dirty_filter):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        clean_filter = dirty_filter.replace("--", "")  # -- is basically required to provide empty filter
        users = Repository().find_all()

        for user in users:
            if clean_filter in user.username:
                print(user.username)

    def delete(self, username):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        Repository().delete_by_username(username)

    def verify_password(self, raw_password, hashed_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
