import csv
from os.path import exists

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_model import Room


class RoomRepository:
    __DB_PATH = 'resources/room_db.csv'
    __fieldnames = ['uuid', 'owner', 'password']

    def __init__(self, participant_repository: ParticipantRepository):
        self.participant_repository = participant_repository

    def save(self, room: Room):
        should_write_headers = False
        if not exists(self.__DB_PATH):
            should_write_headers = True

        with open(self.__DB_PATH, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, self.__fieldnames)

            if should_write_headers:
                writer.writeheader()

            writer.writerow({
                'uuid': room.uuid,
                'owner': room.owner,
                'password': room.password
            })

            csvfile.close()

    def find_by_id(self, room_id):
        with open(self.__DB_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile, self.__fieldnames)

            for row in reader:
                if row['uuid'] == room_id:
                    return Room(
                        row['owner'],
                        row['password'],
                        row['uuid'],
                    )

        return None

    def delete_by_id(self, room_id):
        filtered_rooms = []

        self.participant_repository.delete_by_room_id(room_id)

        with open(self.__DB_PATH, 'r') as read_file:
            reader = csv.DictReader(read_file, self.__fieldnames)

            for row in reader:
                if row['uuid'] != room_id:
                    filtered_rooms.append(row)

        read_file.close()

        with open(self.__DB_PATH, 'w') as write_file:
            writer = csv.DictWriter(write_file, self.__fieldnames)

            for row in filtered_rooms:
                writer.writerow(row)

        write_file.close()
