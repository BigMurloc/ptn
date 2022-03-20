import sys

from user.register import register_user
from user.service import list_all


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
    'list_all': list_all
}

functions_required_number_of_args = {
    'register': 0,
    'list_all': 0
}
