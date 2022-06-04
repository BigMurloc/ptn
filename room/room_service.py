from getpass import getpass
from sqlite3 import IntegrityError

from room.exceptions import AlreadyJoinedRoomException
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

    def create(self, command):
        UserState().is_authenticated()

        if command is None:
            print('Creating room...')
            name = input('Enter name of the room: ')
            password = getpass('Enter room password: ')
            hashed_password = self.password_manager.hash_password(password)
            self.room_repository.save(UserState().user.id, name, self.password_manager.decode(hashed_password))
            return

        hashed_password = self.password_manager.hash_password(command.password)
        decoded_password = self.password_manager.decode(hashed_password)

        self.room_repository.save(UserState().user.id, command.name, decoded_password)

    def find_user_rooms(self, user_id):
        return self.room_repository.find_by_user_id(user_id)

    def join(self, user_id, room_id, password):
        print('Entering room...')
        room: Room = self.room_repository.find_by_id(room_id)

        if self.password_manager.verify_password(password, room.password):
            try:
                self.participant_repository.save(user_id, room.id)
                print(f'Successfully entered the room with id {room.id}')
            except IntegrityError:
                raise AlreadyJoinedRoomException
        else:
            raise RuntimeError('Password did not match')

    def room_summary(self, room_id):
        return self.room_repository.find_summary(room_id)

    def patch_room(self, room_id, topic_id, password):

        if password is not None:
            hashed_password = self.password_manager.hash_password(password)
            password = self.password_manager.decode(hashed_password)

        self.room_repository.patch_room(room_id, topic_id, password)

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

    def vote(self, room_id, user_id, score):
        self.room_repository.vote(room_id, user_id, score)

    def get_votes(self, room_id):
        return self.room_repository.get_votes(room_id)

    def is_owner(self, room_id, user_id=None):
        room: Room = self.room_repository.find_by_id(room_id)

        if user_id is None:
            user_id = UserState().user.id

        return room.owner == user_id

    def is_participant(self, room_id, user_id):
        return self.room_repository.is_participant(room_id, user_id)

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
