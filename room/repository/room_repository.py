from sqlite3 import Connection

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_model import Room


class RoomRepository:
    def __init__(
            self,
            participant_repository: ParticipantRepository,
            db_connection: Connection
    ):
        self.participant_repository = participant_repository
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    def save(self, owner_id, password):
        self.db_cursor.execute("INSERT INTO room (owner, password) VALUES (?, ?)", (owner_id, password))
        self.db_connection.commit()

    def find_by_id(self, room_id):
        self.db_cursor.execute("SELECT * FROM room WHERE id = ? ", (room_id,))
        return self.__room_tuple_mapper(self.db_cursor.fetchone())

    def delete_by_id(self, room_id):
        self.db_cursor.execute("DELETE FROM room WHERE id = ? ", (room_id,))
        self.db_connection.commit()

    def __room_tuple_mapper(self, room_tuple):
        return Room(room_tuple[0], room_tuple[1], room_tuple[2])
