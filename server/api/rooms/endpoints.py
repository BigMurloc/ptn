from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from room.room_service import get_room_service


class My(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):
        service = get_room_service()
        user_rooms = service.find_user_rooms(request.user.display_name)
        return JSONResponse(user_rooms)


rooms_routes = [
    Route('/my', My)
]
