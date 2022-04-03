from dispatcher.commandLineDispatcher import CommandLineDispatcher
from room.repository.participant_repository import ParticipantRepository
from room.repository.room_repository import RoomRepository
from room.room_service import RoomService
from user.repository.user_repository import UserRepository
from util.password_manager import PasswordManager
from user.user_service import UserService

if __name__ == '__main__':
    CommandLineDispatcher(
        UserService(
            UserRepository(),
            PasswordManager()
        ),
        RoomService(
            RoomRepository(
                ParticipantRepository()
            ),
            ParticipantRepository(),
            PasswordManager()
        )
    ).dispatch()
