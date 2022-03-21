from getpass import getpass

import bcrypt

from user.repository import find_by_username
from user.user_state import UserState


def login(username):
    user = find_by_username(username)
    raw_password = getpass()
    if verify_password(raw_password, user.password):
        print('Login success!')
        UserState().is_logged_in = True


def verify_password(raw_password, hashed_password):
    return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
