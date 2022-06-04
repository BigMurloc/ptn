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
            participants.append({'username': room_participant_tuple[0]})

        return {
            'name': user_room_tuple[0],
            'id': user_room_tuple[1],
            'active_topic': user_room_tuple[2],
            'users': participants
        }

    def __active_topic(self, room_id):
        self.db_cursor.execute("SELECT active_topic FROM room WHERE id = ?", (room_id,))
        return self.db_cursor.fetchone()[0]

    def vote(self, room_id, user_id, score):

        active_topic = self.__active_topic(room_id)

        print('topic', active_topic, score)

        self.db_cursor.execute(""
                               "INSERT INTO vote(user_id, topic_id, vote) "
                               "VALUES (?, ?, ?) "
                               "ON CONFLICT (user_id, topic_id) DO UPDATE SET vote = ? ",
                               (user_id, active_topic, score, score)
                               )

        self.db_connection.commit()

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

    def patch_room(self, room_id, topic, password):

        if password is not None:
            self.db_cursor.execute(""
                                   "UPDATE room "
                                   "SET password = ? "
                                   "WHERE id = ? ", (password, room_id))

        if topic is not None:

            self.db_cursor.execute("INSERT INTO topic(room_id, name, description) "
                                   "VALUES (?, ?, '') "
                                   "ON CONFLICT (room_id) DO UPDATE SET name = ? ", (room_id, topic, topic))

            self.db_connection.commit()

            topic_id = self.db_cursor.execute("SELECT id "
                                              "FROM topic "
                                              "WHERE name = ? AND room_id = ?", (topic, room_id)).fetchone()[0]

            self.db_cursor.execute(""
                                   "UPDATE room "
                                   "SET active_topic = ? "
                                   "WHERE id = ? ", (topic_id, room_id))

            self.db_connection.execute(""
                                       "UPDATE vote "
                                       "SET vote = 0 "
                                       "WHERE topic_id = ? ", (topic_id,))

        self.db_connection.commit()

    def get_votes(self, room_id):

        active_topic = self.__active_topic(room_id)

        self.db_cursor.execute(""
                               "SELECT u.username, v.vote "
                               "FROM vote v "
                               "JOIN users u on v.user_id = u.id "
                               "WHERE topic_id = ?",
                               (active_topic,))

        room_vote_tuples = self.db_cursor.fetchall()
        room_votes = []

        for room_vote_tuple in room_vote_tuples:
            room_votes.append(self.__room_vote_tuples_mapper_to_json_object(room_vote_tuple))

        return room_votes

    def is_participant(self, room_id, user_id):
        self.db_cursor.execute("SELECT count(user_id) "
                               "FROM participant "
                               "WHERE room_id = ? AND user_id = ?", (room_id, user_id))
        return self.db_cursor.fetchone()[0] > 0

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

    def __room_vote_tuples_mapper_to_json_object(self, room_vote_tuple):
        return {'username': room_vote_tuple[0], 'value': room_vote_tuple[1]}
