import csv
from getpass import getpass


def register_user():
    name = input("Enter username: ")
    password = getpass()
    if verify_strong_password(password):
        save_user_to_db(name, password)


def save_user_to_db(*data):
    with open('resources/db.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])
        csvfile.close()


# we should also check if file exists and write headers if not

def verify_strong_password(password):
    if len(password) < 8:
        print('Password should be at least 8 characters long')
        return False
    return True
