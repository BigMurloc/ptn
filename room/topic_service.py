from room.repository.topic_repository import TopicRepository


class TopicService:

    def __init__(
            self,
            topic_repository: TopicRepository
    ):
        self.topic_repository = topic_repository

    def create(self, room_id):
        name = input("Topic name: ")
        description = input("Topic description: ")

        self.topic_repository.save(room_id, name, description)

    def delete(self, room_id):
        self.topic_repository.delete(room_id)
