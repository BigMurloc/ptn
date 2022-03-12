import csv
import re
from getpass import getpass

import bcrypt as bcrypt

STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
PASSWORD_INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"


def register_user():
    name = input("Enter username: ")
    password = getpass()
    if verify_password(password):
        save_user_to_db(name, hash_password(password.encode('utf8')))


def save_user_to_db(*data):
    with open('resources/db.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])
        csvfile.close()


# todo we should also check if file exists and write headers if not
def verify_password(password):
    if re.search(PASSWORD_INVALID_CHARACTERS_REGEX, password) is not None:
        return False

    return re.search(STRONG_PASSWORD_REGEX, password) is not None


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))
