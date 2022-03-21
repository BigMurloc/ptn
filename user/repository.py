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
            if row['username'] != 'username':
                users.append(User(row['username'], row['password']))

        return users


def find_by_username(username):
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            if compare_username(row['username'], username):
                return User(row['username'], row['password'])

        return None


def is_username_unique(username):
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)

        for row in reader:
            if compare_username(row['username'], username):
                return False

        return True


def delete_by_username(username):
    filtered_users = []
    with open(DB_PATH, 'r') as read_file:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(read_file, fieldnames)

        for row in reader:
            if not compare_username(row['username'], username):
                filtered_users.append(row)

    with open(DB_PATH, 'w') as write_file:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(write_file, fieldnames)

        for row in filtered_users:
            writer.writerow(row)


def compare_username(u1, u2):
    return u1.lower() == u2.lower()
