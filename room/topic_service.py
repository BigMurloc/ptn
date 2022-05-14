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
        if not self.room_service.is_owner(room_id):
            raise RuntimeError('You are not owner of this room')

        name = input("Topic name: ")
        description = input("Topic description: ")

        self.topic_repository.delete(room_id)
        topic_id = self.topic_repository.save(room_id, name, description)
        self.room_service.set_active_topic(topic_id, room_id)

    def delete(self, room_id):
        if not self.room_service.is_owner(room_id):
            raise RuntimeError('You are not owner of this room')

        self.room_service.set_active_topic(None, room_id)
        self.topic_repository.delete(room_id)
