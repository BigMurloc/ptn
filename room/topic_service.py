from room.repository.topic_repository import TopicRepository
from room.room_service import RoomService


class TopicService:

    def __init__(
            self,
            room_service: RoomService,
            topic_repository: TopicRepository
    ):
        self.topic_repository = topic_repository
        self.room_service = room_service

    def create(self, room_id):
        name = input("Topic name: ")
        description = input("Topic description: ")

        if self.room_service.is_owner(room_id):
            self.topic_repository.delete(room_id)
            topic_id = self.topic_repository.save(room_id, name, description)
            self.room_service.set_active_topic(topic_id, room_id)
        else:
            raise RuntimeError('You are not owner of this room')

    def delete(self, room_id):
        self.topic_repository.delete(room_id)
