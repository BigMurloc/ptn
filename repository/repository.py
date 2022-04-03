import csv
from os.path import exists


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Repository:
    DB_PATH = 'resources/db.csv'

    def find_all(self):
        with open(self.DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)

            users = []

            for row in reader:
                if row['username'] != 'username':
                    users.append(User(row['username'], row['password']))

            return users

    def find_by_username(self, username):
        with open(self.DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                if self.compare_username(row['username'], username):
                    return User(row['username'], row['password'])

            return None

    def save(self, username, hashed_password):
        should_write_headers = False
        if not exists(self.DB_PATH):
            should_write_headers = True

        with open(self.DB_PATH, 'a') as csvfile:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames)

            if should_write_headers:
                writer.writeheader()

            writer.writerow({'username': username, 'password': hashed_password})
            csvfile.close()

    def delete_by_username(self, username):
        filtered_users = []
        with open(self.DB_PATH, 'r') as read_file:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(read_file, fieldnames)

            for row in reader:
                if not self.compare_username(row['username'], username):
                    filtered_users.append(row)

        with open(self.DB_PATH, 'w') as write_file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(write_file, fieldnames)

            for row in filtered_users:
                writer.writerow(row)

    def is_username_unique(self, username):
        with open(self.DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)

            for row in reader:
                if self.compare_username(row['username'], username):
                    return False

            return True

    def compare_username(self, u1, u2):
        return u1.lower() == u2.lower()
