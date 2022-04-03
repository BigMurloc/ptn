import re
from getpass import getpass


from repository.repository import Repository
from user.user_state import UserState
from user.password_manager import PasswordManager


class UserService:
    STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"

    def register(self):
        username = self.get_username()
        password = self.get_password()

        hashed_password = PasswordManager().hash_password(password)

        Repository().save(username.lower(), PasswordManager().decode(hashed_password))

    def login(self, username):
        user = Repository().find_by_username(username)
        raw_password = getpass()
        if PasswordManager().verify_password(raw_password, user.password):
            print('Login success!')
            UserState().is_logged_in = True
        else:
            print('Login failure')

    def list_all(self, dirty_filter):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        clean_filter = dirty_filter.replace("--", "")  # -- is basically required to provide empty filter
        users = Repository().find_all()

        for user in users:
            if clean_filter in user.username:
                print(user.username)

    def delete(self, username):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        Repository().delete_by_username(username)

    def get_username(self):
        username = input("Enter username: ")
        while self.verify_username(username) is not True:
            username = input("Enter username: ")
        return username

    def get_password(self):
        password = getpass()
        while self.check_password_strength(password) is not True:
            password = getpass()
        return password

    def verify_username(self, username):
        if re.search(self.INVALID_CHARACTERS_REGEX, username) is not None:
            print("Username contains invalid characters, please try again")
            return False

        if Repository().is_username_unique(username) is False:
            print("Username is already taken")
            return False

        return True

    def check_password_strength(self, password):
        if re.search(self.INVALID_CHARACTERS_REGEX, password) is not None:
            print("Password contains invalid characters like whitespace, please try again")
            return False

        if re.search(self.STRONG_PASSWORD_REGEX, password) is None:
            print("Password is not strong enough, "
                  "password should be at least 8 characters long and include one of each: "
                  "cipher, upper letter, lower letter ")
            return False

        return True

