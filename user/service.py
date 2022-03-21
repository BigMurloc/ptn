from user.repository import find_all, delete_by_username
from user.user_state import UserState


def list_all():
    if not UserState().is_logged_in:
        raise RuntimeError('You are not authorized to do this operation')

    users = find_all()

    for user in users:
        print(user.username)


def delete(username):
    # if not UserState().is_logged_in:
    #     raise RuntimeError('You are not authorized to do this operation')

    delete_by_username(username)
