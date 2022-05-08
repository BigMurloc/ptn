from sqlite3 import Connection


class TopicRepository:
    def __init__(self, db_connection: Connection):
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    def save(self, room_id, name, description):
        self.db_cursor.execute(
            "INSERT INTO topic (room_id, name, description) VALUES (?, ?, ?)", (room_id, name, description)
        )
        self.db_connection.commit()

    def delete(self, room_id):
        self.db_cursor.execute("DELETE FROM topic WHERE room_id = ?", (room_id,))
