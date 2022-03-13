import csv
from os.path import exists

DB_PATH = 'resources/db.csv'


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


def is_username_unique(username):
    with open(DB_PATH, 'r') as csvfile:
        fieldnames = ['username', 'password']
        reader = csv.DictReader(csvfile, fieldnames)

        for row in reader:
            if row['username'] == username:
                return False

        return True
