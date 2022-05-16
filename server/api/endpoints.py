from starlette.routing import Mount
from server.api.users.endpoints import routes

routes = [
     Mount('/users', routes=routes)
 ]