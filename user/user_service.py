from getpass import getpass

from user.exceptions import UserDataValidationError, AuthenticationError
from user.repository.user_model import User
from user.repository.user_repository import UserRepository
from user.user_guard import UserGuard
from user.user_state import UserState
from util.database import get_database
from util.password_manager import PasswordManager


class UserService:

    def __init__(
            self,
            repository: UserRepository,
            password_manager: PasswordManager
    ):
        self.repository = repository
        self.user_guard = UserGuard(repository)
        self.password_manager = password_manager

    def register(self):
        username = self.__get_username()
        password = self.__get_password()

        hashed_password = self.password_manager.hash_password(password)

        self.repository.save(username, self.password_manager.decode(hashed_password))

    def register(self, username, password):
        if not self.user_guard.verify_username(username) or not self.user_guard.check_password_strength(password):
            raise UserDataValidationError

        hashed_password = self.password_manager.hash_password(password)

        self.repository.save(username, self.password_manager.decode(hashed_password))

    def login(self, username, password):
        user = self.repository.find_by_username(username)
        if self.password_manager.verify_password(password, user.password):
            print('Login success!')
            UserState().is_logged_in = True
            UserState().user = user
        else:
            UserState().is_logged_in = False
            raise AuthenticationError('Login failure')

    def list_all(self, user_filter):
        UserState().is_authenticated()

        users = self.repository.find_all()

        for user in users:
            if user_filter is None or user_filter in user.user:
                print(user.username)

    def delete(self, username):
        UserState().is_authenticated()

        self.repository.delete_by_username(username)

    def __get_username(self):
        username = input("Enter username: ")
        while self.user_guard.verify_username(username) is not True:
            username = input("Enter username: ")
        return username

    def __get_password(self):
        password = getpass()
        while self.user_guard.check_password_strength(password) is not True:
            password = getpass()
        return password


def get_user_service():
    return UserService(
        UserRepository(
            get_database()
        ),
        PasswordManager()
    )
