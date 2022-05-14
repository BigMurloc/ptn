from room.repository.topic_repository import TopicRepository
from room.room_service import RoomService


class TopicService:
    __allowed_voting_values = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 50, 100, 200, -1, -2]

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

    def vote(self, room_id, score):
        if float(score) not in self.__allowed_voting_values:
            print('Allowed voting values:')
            for voting_value in self.__allowed_voting_values:
                print(voting_value)
            raise RuntimeError('Score not within allowed values')

        self.topic_repository.vote(room_id, float(score))

    def delete(self, room_id):
        if not self.room_service.is_owner(room_id):
            raise RuntimeError('You are not owner of this room')

        self.room_service.set_active_topic(None, room_id)
        self.topic_repository.delete(room_id)
