import click

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_repository import RoomRepository
from room.room_service import RoomService
from user.repository.user_repository import UserRepository
from user.user_service import UserService
from util.database import get_database, init_db
from util.password_manager import PasswordManager


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {'db': get_database()}


# ----------------------CLI--------------------

@cli.command(help="Register user")
@click.pass_obj
def register(obj):
    UserService(
        UserRepository(obj['db']),
        PasswordManager()
    ).register()


@cli.command("init-db", help="Sets up a new database, erasing all the data")
@click.pass_obj
def initialize_db(obj):
    init_db(obj['db'])


@cli.group("user", help="Provide login and password")
@click.option("--username", required=True)
@click.password_option()
@click.pass_obj
def user(obj, username, password):
    UserService(
        UserRepository(obj['db']),
        PasswordManager()
    ).login(username, password)


# ----------------------USER-------------------


@user.command()
@click.option("--filter")
@click.pass_obj
def list_all(obj, filter):
    UserService(
        UserRepository(obj['db']),
        PasswordManager()
    ).list_all(filter)


@user.command()
@click.option("--username", required=True)
@click.pass_obj
def delete(obj, username):
    UserService(
        UserRepository(obj['db']),
        PasswordManager()
    ).delete(username)


@user.command()
@click.pass_obj
def make_room(obj):
    participant_repository = ParticipantRepository(obj['db'])
    RoomService(
        RoomRepository(
            participant_repository,
            obj['db']
        ),
        participant_repository,
        PasswordManager()
    ).create()


@user.command()
@click.option("--room_id", required=True)
@click.pass_obj
def delete_room(obj, room_id):
    participant_repository = ParticipantRepository(obj['db'])
    RoomService(
        RoomRepository(
            participant_repository,
            obj['db']
        ),
        participant_repository,
        PasswordManager()
    ).delete(room_id)


@user.group("room")
@click.option("--room_id", required=True)
@click.password_option("--room_password")
@click.pass_obj
def room(obj, room_id, room_password):
    participant_repository = ParticipantRepository(obj['db'])
    RoomService(
        RoomRepository(
            participant_repository,
            obj['db']
        ),
        participant_repository,
        PasswordManager()
    ).join(room_id, room_password)


# ----------------------ROOM------------------

@room.command("create-topic", help="Creates a new room topic")
def create_topic():
    pass


@room.command("delete-topic", help="Deletes room topic")
def delete_topic():
    pass


@room.command("change-topic", help="Changes room topic")
def change_topic():
    pass


@room.command("vote",
              help="Votes for current room topic. Accepted values: 0, ½, 1, 2, 3, 5, 8, 13, 20, 50, 100, 200, -1, -2")
def vote():
    pass


if __name__ == '__main__':
    cli()

# TODO: increase readability of user prompts and command help descriptions
# TODO: allow user to delete himself
