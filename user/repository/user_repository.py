import csv
from os.path import exists

from user.repository.user_model import User


class UserRepository:
    __DB_PATH = 'resources/user_db.csv'

    def find_all(self):
        with open(self.__DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)

            users = []

            for row in reader:
                if row['username'] != 'username':
                    users.append(User(row['username'], row['password']))

            return users

    def find_by_username(self, username):
        with open(self.__DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                if self.__compare_username(row['username'], username):
                    return User(row['username'], row['password'])

            return None

    def save(self, user):
        should_write_headers = False
        if not exists(self.__DB_PATH):
            should_write_headers = True

        with open(self.__DB_PATH, 'a') as csvfile:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames)

            if should_write_headers:
                writer.writeheader()

            writer.writerow({'username': user.username, 'password': user.password})
            csvfile.close()

    def delete_by_username(self, username):
        filtered_users = []
        with open(self.__DB_PATH, 'r') as read_file:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(read_file, fieldnames)

            for row in reader:
                if not self.__compare_username(row['username'], username):
                    filtered_users.append(row)

        with open(self.__DB_PATH, 'w') as write_file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(write_file, fieldnames)

            for row in filtered_users:
                writer.writerow(row)

    def is_username_unique(self, username):
        with open(self.__DB_PATH, 'r') as csvfile:
            fieldnames = ['username', 'password']
            reader = csv.DictReader(csvfile, fieldnames)

            for row in reader:
                if self.__compare_username(row['username'], username):
                    return False

            return True

    def __compare_username(self, u1, u2):
        return u1.lower() == u2.lower()
