import csv
import re
from getpass import getpass

STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[#!@$]).{8,}$"


def register_user():
    name = input("Enter username: ")
    password = getpass()
    if verify_password(password):
        save_user_to_db(name, password)
    else:
        print("Password should contain at least "
              "one upper letter, "
              "one lower letter, "
              "one cipher "
              "and at least one of ! @ # $ ")


def save_user_to_db(*data):
    with open('resources/db.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])
        csvfile.close()


# todo we should also check if file exists and write headers if not
# todo check password for invalid characters
# todo save hashed password
def verify_password(password):
    return re.search(STRONG_PASSWORD_REGEX, password) is not None


