import sys

from user.login import login
from user.register import register_user
from user.service import list_all, delete
from user.user_state import UserState


def dispatch():
    number_of_args = len(sys.argv)
    command_index = 1
    command_index_registry = []
    while command_index < number_of_args:
        functions[sys.argv[command_index]]  # check if exists in dict and throw error if does not.
        command_index_registry.append(command_index)
        command_index += functions_required_number_of_args[sys.argv[command_index]] + 1

    for command_index in command_index_registry:
        execute(command_index)


def execute(command_index):
    number_of_required_arguments = functions_required_number_of_args[sys.argv[command_index]]

    function_args = []
    incrementer = 1
    while len(function_args) < number_of_required_arguments:
        function_args.append(sys.argv[command_index + incrementer])
        incrementer += 1

    functions[sys.argv[command_index]](*function_args)


functions = {
    'register': register_user,
    'login': login,
    'list_all': list_all,
    'delete': delete
}

functions_required_number_of_args = {
    'register': 0,
    'login': 1,
    'list_all': 1,
    'delete': 1
}
