import csv
from os.path import exists

from room.repository.participant_model import Participant


class ParticipantRepository:
    __DB_PATH = 'resources/participant_db'
    __fieldnames = ['user_id', 'room_id']

    def save(self, participant: Participant):
        should_write_headers = False
        if not exists(self.__DB_PATH):
            should_write_headers = True

        with open(self.__DB_PATH, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, self.__fieldnames)

            if should_write_headers:
                writer.writeheader()

            writer.writerow({
                'user_id': participant.user_id,
                'room_id': participant.room_id
            })

            csvfile.close()

    def find_participants_by_room_id(self, room_id):
        result = []

        with open(self.__DB_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile, self.__fieldnames)

            for row in reader:
                if row['room_id'] == room_id:
                    result.append(Participant(row['user_id'], row['room_id']))
        csvfile.close()

        return result

    def delete_by_room_id(self, room_id):
        filtered_participants = []

        with open(self.__DB_PATH, 'r') as read_file:
            reader = csv.DictReader(read_file, self.__fieldnames)

            for row in reader:
                if row['room_id'] != room_id:
                    filtered_participants.append(row)

        read_file.close()

        with open(self.__DB_PATH, 'w') as write_file:
            writer = csv.DictWriter(write_file, self.__fieldnames)

            for row in filtered_participants:
                writer.writerow(row)

        write_file.close()
