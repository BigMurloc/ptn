from getpass import getpass


from repository.repository import Repository
from user.user_state import UserState
from user.password_manager import PasswordManager
from user.user_guard import UserGuard


class UserService:

    def __init__(
            self,
            repository: Repository,
            user_guard: UserGuard,
            password_manager: PasswordManager
    ):
        self.repository = repository
        self.user_guard = user_guard
        self.password_manager = password_manager

    def register(self):
        username = self.__get_username()
        password = self.__get_password()

        hashed_password = self.password_manager.hash_password(password)

        self.repository.save(username.lower(), self.password_manager.decode(hashed_password))

    def login(self, username):
        user = self.repository.find_by_username(username)
        raw_password = getpass()
        if self.password_manager.verify_password(raw_password, user.password):
            print('Login success!')
            UserState().is_logged_in = True
        else:
            UserState().is_logged_in = False
            print('Login failure')

    def list_all(self, dirty_filter):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        clean_filter = dirty_filter.replace("--", "")  # -- is basically required to provide empty filter
        users = self.repository.find_all()

        for user in users:
            if clean_filter in user.username:
                print(user.username)

    def delete(self, username):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

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

