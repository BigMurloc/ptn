from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route


class Login(HTTPEndpoint):

    async def get(self, request):
        return JSONResponse({'login': 'dunno'})


routes = [
    Route('/login', Login)
]
