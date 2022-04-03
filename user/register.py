import re
from getpass import getpass

import bcrypt as bcrypt

from repository.repository import Repository

STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"


def register_user():
    username = get_username()
    password = get_password()

    Repository().save(username.lower(), hash_password(password.encode('utf8')).decode('utf-8'))


def get_username():
    username = input("Enter username: ")
    while verify_username(username) is not True:
        username = input("Enter username: ")
    return username


def get_password():
    password = getpass()
    while verify_password(password) is not True:
        password = getpass()
    return password


def verify_username(username):
    if re.search(INVALID_CHARACTERS_REGEX, username) is not None:
        print("Username contains invalid characters, please try again")
        return False

    if Repository().is_username_unique(username) is False:
        print("Username is already taken")
        return False

    return True


def verify_password(password):
    if re.search(INVALID_CHARACTERS_REGEX, password) is not None:
        print("Password contains invalid characters like whitespace, please try again")
        return False

    if re.search(STRONG_PASSWORD_REGEX, password) is None:
        print("Password is not strong enough, "
              "password should be at least 8 characters long and include one of each: "
              "cipher, upper letter, lower letter ")
        return False

    return True


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())
