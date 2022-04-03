import sys

from user.user_service import UserService


class Dispatcher:

    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.__functions = {
            'register': self.user_service.register,
            'login': self.user_service.login,
            'list_all': self.user_service.list_all,
            'delete': self.user_service.delete
        }
        self.__functions_required_number_of_args = {
            'register': 0,
            'login': 1,
            'list_all': 1,
            'delete': 1
        }

    def dispatch(self):
        number_of_args = len(sys.argv)
        command_index = 1
        command_index_registry = []
        while command_index < number_of_args:
            self.__functions[sys.argv[command_index]]  # check if exists in dict and throw error if does not.
            command_index_registry.append(command_index)
            command_index += self.__functions_required_number_of_args[sys.argv[command_index]] + 1

        for command_index in command_index_registry:
            self.__execute(command_index)

    def __execute(self, command_index):
        number_of_required_arguments = self.__functions_required_number_of_args[sys.argv[command_index]]

        function_args = []
        incrementer = 1
        while len(function_args) < number_of_required_arguments:
            function_args.append(sys.argv[command_index + incrementer])
            incrementer += 1

        self.__functions[sys.argv[command_index]](*function_args)
