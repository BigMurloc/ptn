from dispatcher.commandLineDispatcher import CommandLineDispatcher
from user.repository.user_repository import UserRepository
from user.password_manager import PasswordManager
from user.user_service import UserService

if __name__ == '__main__':
    CommandLineDispatcher(
        UserService(
            UserRepository(),
            PasswordManager()
        )
    ).dispatch()
