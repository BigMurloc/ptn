from getpass import getpass

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_model import Room
from room.repository.room_repository import RoomRepository
from user.user_state import UserState
from util.database import get_database
from util.password_manager import PasswordManager


class RoomService:

    def __init__(
            self,
            room_repository: RoomRepository,
            participant_repository: ParticipantRepository,
            password_manager: PasswordManager
    ):
        self.room_repository = room_repository
        self.participant_repository = participant_repository
        self.password_manager = password_manager

    def create(self):
        UserState().is_authenticated()

        print('Creating room...')
        password = getpass('Enter room password: ')
        hashed_password = self.password_manager.hash_password(password)

        self.room_repository.save(UserState().user.id, self.password_manager.decode(hashed_password))

    def find_user_rooms(self, user_id):
        return self.room_repository.find_by_user_id(user_id)

    def join(self, room_id, password):
        print('Entering room...')
        room: Room = self.room_repository.find_by_id(room_id)

        if self.password_manager.verify_password(password, room.password):
            self.participant_repository.save(UserState().user.id, room.id)
            print(f'Successfully entered the room with id {room.id}')
        else:
            raise RuntimeError('Password did not match')

    def delete(self, room_id):
        UserState().is_authenticated()

        print('Deleting room...')
        room: Room = self.room_repository.find_by_id(room_id)

        if room.owner == UserState().user.id:
            self.room_repository.delete_by_id(room_id)
            self.participant_repository.delete_by_room_id(room_id)
            print(f'Successfully deleted the room with id {room_id}')
        else:
            raise RuntimeError('You are not owner of this room')

    def is_owner(self, room_id):
        room: Room = self.room_repository.find_by_id(room_id)

        return room.owner == UserState().user.id

    def set_active_topic(self, topic_id, room_id):
        self.room_repository.set_active_topic(topic_id, room_id)


def get_room_service():
    db_conn = get_database()
    return RoomService(
        RoomRepository(
            ParticipantRepository(
                db_conn
            ),
            db_conn
        ),
        ParticipantRepository(
            db_conn
        ),
        PasswordManager()
    )
