from user.repository import find_all


def list_all():
    users = find_all()

    for user in users:
        print(user.username)

