from dispatcher.commandLineDispatcher import CommandLineDispatcher
from repository.repository import Repository
from user.password_manager import PasswordManager
from user.user_guard import UserGuard
from user.user_service import UserService

if __name__ == '__main__':
    CommandLineDispatcher(
        UserService(
            Repository(),
            UserGuard(),
            PasswordManager()
        )
    ).dispatch()
