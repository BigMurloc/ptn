import click

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_repository import RoomRepository
from room.room_service import RoomService
from user.repository.user_repository import UserRepository
from user.user_service import UserService
from util.password_manager import PasswordManager


@click.group()
def cli():
    pass


# ----------------------CLI--------------------

@cli.command(help="Register user")
def register():
    UserService(
        UserRepository(),
        PasswordManager()
    ).register()


# ----------------------USER-------------------

@cli.group("user", help="Provide login and password")
@click.option("--username", required=True)
@click.password_option()
def user(username, password):
    UserService(
        UserRepository(),
        PasswordManager()
    ).login(username, password)


@user.command()
@click.option("--filter")
def list_all(filter):
    UserService(
        UserRepository(),
        PasswordManager()
    ).list_all(filter)


@user.command()
@click.option("--username", required=True)
def delete(username):
    UserService(
        UserRepository(),
        PasswordManager()
    ).delete(username)


# ----------------------ROOM------------------

@user.command()
def make_room():
    participant_repository = ParticipantRepository()
    RoomService(
        RoomRepository(
            participant_repository
        ),
        participant_repository,
        PasswordManager()
    ).create()


@user.command()
@click.option("--room_id", required=True)
@click.password_option("--room_password")
def join_room(room_id, room_password):
    participant_repository = ParticipantRepository()
    RoomService(
        RoomRepository(
            participant_repository
        ),
        participant_repository,
        PasswordManager()
    ).join(room_id, room_password)


@user.command()
@click.option("--room_id", required=True)
def delete_room(room_id):
    participant_repository = ParticipantRepository()
    RoomService(
        RoomRepository(
            participant_repository
        ),
        participant_repository,
        PasswordManager()
    ).delete(room_id)


if __name__ == '__main__':
    cli()

# TODO: increase readability of user prompts and command help descriptions
# TODO: refactor commands to make it more aligned with @click (make use of passing the command context)
# TODO: allow user to delete himself
