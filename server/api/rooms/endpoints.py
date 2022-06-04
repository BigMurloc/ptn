from pydantic import ValidationError
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from room.exceptions import AlreadyJoinedRoomException
from room.room_service import get_room_service
from server.api.rooms.dto.room_create_command import RoomCreateCommand
from server.api.rooms.dto.room_join_command import RoomJoinCommand
from server.api.rooms.dto.room_patch_command import RoomPatchCommand
from server.api.rooms.dto.room_vote_command import RoomVoteCommand


class My(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):
        service = get_room_service()
        user_rooms = service.find_user_rooms(request.user.display_name)
        return JSONResponse(user_rooms)


class Create(HTTPEndpoint):

    @requires('authenticated')
    async def post(self, request):
        body = await request.json()
        try:
            command = RoomCreateCommand(**body)
        except ValidationError:
            return JSONResponse({}, status_code=400)

        service = get_room_service()
        service.create(command)

        return JSONResponse({}, status_code=201)


class Join(HTTPEndpoint):

    @requires('authenticated')
    async def post(self, request):
        room_id = request.path_params.get('id')
        body = await request.json()

        try:
            command = RoomJoinCommand(**body)
        except ValidationError:
            return JSONResponse({}, status_code=400)

        service = get_room_service()
        try:
            service.join(request.user.display_name, room_id, command.password)
        except AlreadyJoinedRoomException:
            return JSONResponse({'error': 'already joined'}, status_code=409)

        return JSONResponse({})


class Room(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):
        service = get_room_service()

        room_id = request.path_params.get('id')
        user_id = request.user.display_name
        if not service.is_participant(room_id, user_id) and not service.is_owner(room_id, user_id):
            return JSONResponse({'error': 'not participant'}, status_code=403)

        summary = service.room_summary(room_id)
        return JSONResponse(summary)

    @requires('authenticated')
    async def patch(self, request):

        service = get_room_service()
        room_id = request.path_params.get('id')
        user_id = request.user.display_name

        if not service.is_owner(room_id, user_id):
            return JSONResponse({'error': 'not owner'}, status_code=403)

        body = await request.json()

        command = RoomPatchCommand(**body)

        service.patch_room(room_id, command.topic_id, command.password)
        summary = service.room_summary(room_id)

        return JSONResponse(summary)


class Vote(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):

        service = get_room_service()
        user_id = request.user.display_name
        room_id = request.path_params.get('id')

        if not service.is_participant(room_id, user_id):
            return JSONResponse({'error': 'not participant'}, status_code=403)

        room_votes = service.get_votes(room_id)

        return JSONResponse({'votes': room_votes})

    @requires('authenticated')
    async def put(self, request):

        service = get_room_service()
        room_id = request.path_params.get('id')
        user_id = request.user.display_name

        if not service.is_participant(room_id, user_id):
            return JSONResponse({'error': 'not participant'}, status_code=403)

        body = await request.json()
        try:
            command = RoomVoteCommand(**body)
        except ValidationError:
            return JSONResponse({}, status_code=400)

        service.vote(room_id, user_id, command.vote)

        return JSONResponse({})


rooms_routes = [
    Route('/my', My),
    Route('/create', Create),
    Route('/{id}/join', Join),
    Route('/{id}', Room),
    Route('/{id}/vote', Vote)
]
