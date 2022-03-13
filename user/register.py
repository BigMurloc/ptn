import re
from getpass import getpass

import bcrypt as bcrypt

from user.repository import save

STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"


# todo loop user over and over if password does not match requirements
def register_user():
    username = input("Enter username: ")
    password = getpass()
    if verify_password(password) and verify_username(username):
        save(username, hash_password(password.encode('utf8')))


def verify_username(username):
    return re.search(INVALID_CHARACTERS_REGEX, username) is None


def verify_password(password):
    if re.search(INVALID_CHARACTERS_REGEX, password) is not None:
        return False

    return re.search(STRONG_PASSWORD_REGEX, password) is not None


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))
