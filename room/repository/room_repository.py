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

    def save(self, owner_id, name, password):
        self.db_cursor.execute("INSERT INTO room (owner, name, password) VALUES (?, ?, ?)", (owner_id, name, password))
        self.db_connection.commit()

    def find_by_id(self, room_id):
        self.db_cursor.execute("SELECT * FROM room WHERE id = ? ", (room_id,))
        return self.__room_tuple_mapper(self.db_cursor.fetchone())

    def find_summary(self, room_id):
        self.db_cursor.execute("SELECT u.username, r.id, r.active_topic "
                               "FROM room r "
                               "JOIN users u on r.owner = u.id "
                               "WHERE r.id = ? ", (room_id,))
        user_room_tuple = self.db_cursor.fetchone()

        self.db_cursor.execute("SELECT u.username "
                               "FROM participant p "
                               "JOIN users u on p.user_id = u.id "
                               "WHERE p.room_id = ?", (room_id,))

        room_participants_tuples = self.db_cursor.fetchall()

        participants = []

        for room_participant_tuple in room_participants_tuples:
            participants.append({'username':  room_participant_tuple[0]})

        return {
            'name': user_room_tuple[0],
            'id': user_room_tuple[1],
            'active_topic': user_room_tuple[2],
            'users': participants
        }

    def find_by_user_id(self, user_id):
        self.db_cursor.execute(""
                               "SELECT u1.username, r1.id, u1.username "
                               "FROM room r1 "
                               "JOIN users u1 on u1.id = r1.owner "
                               "WHERE r1.owner = ? "
                               "UNION "
                               "SELECT u2.username, r2.id, o.username "
                               "FROM participant p "
                               "JOIN users u2 on u2.id = p.user_id "
                               "JOIN room r2 on r2.id = p.room_id "
                               "JOIN users o on o.id = r2.owner "
                               "WHERE p.user_id = ?",
                               (user_id, user_id))

        user_room_tuples = self.db_cursor.fetchall()
        user_rooms = []

        for user_room_tuple in user_room_tuples:
            user_rooms.append(self.__user_room_tuple_mapper_to_json_object(user_room_tuple))

        return user_rooms

    def delete_by_id(self, room_id):
        self.db_cursor.execute("DELETE FROM room WHERE id = ? ", (room_id,))
        self.db_connection.commit()

    def set_active_topic(self, topic_id, room_id):
        self.db_cursor.execute(""
                               "UPDATE room SET active_topic = ? WHERE id = ?", (topic_id, room_id))
        self.db_connection.commit()

    def __room_tuple_mapper(self, room_tuple):
        return Room(room_tuple[0], room_tuple[1], room_tuple[2], room_tuple[3])

    def __user_room_tuple_mapper_to_json_object(self, user_room_tuple):
        return {'name': user_room_tuple[0], 'id': user_room_tuple[1], 'owner': user_room_tuple[2]}
