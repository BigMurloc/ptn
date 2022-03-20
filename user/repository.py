import csv
from os.path import exists

DB_PATH = 'resources/db.csv'


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def save(username, hashed_password):
    should_write_headers = False
    if not exists(DB_PATH):
        should_write_headers = True

    with open(DB_PATH, 'a') as csvfile:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames)

        if should_write_headers:
            writer.writeheader()

        writer.writerow({'username': username, 'password': hashed_password})
        csvfile.close()


def find_all():
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)

        users = []

        for row in reader:
            users.append(User(row['username'], row['password']))

        return users


def find_by_username(username):
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)

        for row in reader:
            if row['username'] == username:
                return User(row['username', row['password']])

        return None


def is_username_unique(username):
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)

        for row in reader:
            if row['username'] == username:
                return False

        return True
