from pydantic import ValidationError
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from room.room_service import get_room_service
from server.api.rooms.dto.room_create_command import RoomCreateCommand
from server.api.rooms.dto.room_join_command import RoomJoinCommand


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
            return JSONResponse('some fields are missing', status_code=400)

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
            return JSONResponse('some fields are missing', status_code=400)

        service = get_room_service()
        service.join(request.user.display_name, room_id, command.password)

        return JSONResponse({})


class Get(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):
        service = get_room_service()
        summary = service.room_summary(request.path_params.get('id'))
        return JSONResponse(summary)


rooms_routes = [
    Route('/my', My),
    Route('/create', Create),
    Route('/{id}/join', Join),
    Route('/{id}', Get)
]
