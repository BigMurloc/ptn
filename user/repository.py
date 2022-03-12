import csv

DB_PATH = 'resources/db.csv'


def save(*data):
    with open(DB_PATH, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([*data])
        csvfile.close()
