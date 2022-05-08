from sqlite3 import Connection

from room.repository.participant_model import Participant


class ParticipantRepository:
    def __init__(self, db_connection: Connection):
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    def save(self, participant_id, room_id):
        self.db_cursor.execute(
            "INSERT INTO participant (user_id, room_id) VALUES (?, ?)", (participant_id, room_id)
        )

        self.db_connection.commit()

    def delete_by_room_id(self, room_id):
        self.db_cursor.execute("DELETE FROM participant WHERE room_id = ?", (room_id,))
        self.db_connection.commit()

    def __participant_tuple_mapper(self, participant_tuple):
        return Participant(participant_tuple[0], participant_tuple[1], participant_tuple[2])
