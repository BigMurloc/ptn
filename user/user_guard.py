import re

from repository.repository import Repository


class UserGuard:

    __STRONG_PASSWORD_REGEX = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    __INVALID_CHARACTERS_REGEX = "^(?=.*\\s)"

    def verify_username(self, username):
        if re.search(self.__INVALID_CHARACTERS_REGEX, username) is not None:
            print("Username contains invalid characters, please try again")
            return False

        if Repository().is_username_unique(username) is False:
            print("Username is already taken")
            return False

        return True

    def check_password_strength(self, password):
        if re.search(self.__INVALID_CHARACTERS_REGEX, password) is not None:
            print("Password contains invalid characters like whitespace, please try again")
            return False

        if re.search(self.__STRONG_PASSWORD_REGEX, password) is None:
            print("Password is not strong enough, "
                  "password should be at least 8 characters long and include one of each: "
                  "cipher, upper letter, lower letter ")
            return False

        return True
