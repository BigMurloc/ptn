import re
from getpass import getpass

import bcrypt as bcrypt

from user.repository import save

STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
PASSWORD_INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"


# todo loop user over and over if password does not match requirements
def register_user():
    name = input("Enter username: ")
    password = getpass()
    if verify_password(password):
        save(name, hash_password(password.encode('utf8')))


def verify_username(username):
    # todo invalid characters
    pass


def verify_password(password):
    if re.search(PASSWORD_INVALID_CHARACTERS_REGEX, password) is not None:
        return False

    return re.search(STRONG_PASSWORD_REGEX, password) is not None


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))
