from starlette.routing import Mount

from server.api.rooms.endpoints import rooms_routes
from server.api.users.endpoints import user_routes

api_routes = [
    Mount('/users', routes=user_routes),
    Mount('/rooms', routes=rooms_routes)
]
