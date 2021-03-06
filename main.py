import os

import click

from room.repository.participant_repository import ParticipantRepository
from room.repository.room_repository import RoomRepository
from room.repository.topic_repository import TopicRepository
from room.room_service import RoomService
from room.topic_service import TopicService
from server import run
from user.repository.user_repository import UserRepository
from user.user_service import UserService
from user.user_state import UserState
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


@cli.command("run-as-server", help="Runs program as api server")
def run_as_server():
    run()


# ----------------------USER-------------------


@user.command()
@click.option("--filter")
@click.pass_obj
def list_all(obj, filter):
    UserState().is_authenticated()

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
    obj['room_id'] = room_id
    participant_repository = ParticipantRepository(obj['db'])
    RoomService(
        RoomRepository(
            participant_repository,
            obj['db']
        ),
        participant_repository,
        PasswordManager()
    ).join(UserState().user.id, room_id, room_password)


# ----------------------ROOM------------------

@room.command("change-topic", help="Creates a new room topic")
@click.pass_obj
def create_topic(obj):
    TopicService(
        RoomService(
            RoomRepository(
                ParticipantRepository(obj['db']),
                obj['db']
            ),
            ParticipantRepository(
                obj['db']
            ),
            obj['db'],
        ),
        TopicRepository(
            obj['db']
        ),
    ).create(obj['room_id'])


@room.command("delete-topic", help="Deletes room topic")
@click.pass_obj
def delete_topic(obj):
    TopicService(
        RoomService(
            RoomRepository(
                ParticipantRepository(obj['db']),
                obj['db']
            ),
            ParticipantRepository(
                obj['db']
            ),
            obj['db'],
        ),
        TopicRepository(
            obj['db']
        ),
    ).delete(obj['room_id'])


@room.command("vote",
              help="Votes for current room topic. Accepted values: 0, ??, 1, 2, 3, 5, 8, 13, 20, 50, 100, 200, -1, -2")
@click.pass_obj
@click.option("--score")
def vote(obj, score):
    TopicService(
        RoomService(
            RoomRepository(
                ParticipantRepository(obj['db']),
                obj['db']
            ),
            ParticipantRepository(
                obj['db']
            ),
            obj['db'],
        ),
        TopicRepository(
            obj['db']
        ),
    ).vote(obj['room_id'], score)


if __name__ == '__main__':
    cli()

# TODO: increase readability of user prompts and command help descriptions
# TODO: allow user to delete himself
