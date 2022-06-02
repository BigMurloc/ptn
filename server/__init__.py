import jwt
import uvicorn
from jwt import ExpiredSignatureError
from starlette.applications import Starlette
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount

from server.api.endpoints import api_routes


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "authorization" not in conn.headers:
            return
        auth = conn.headers["authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'jwt':
                return
            decoded = jwt.decode(credentials, 'secret', algorithms='HS256')
        except ExpiredSignatureError:
            raise AuthenticationError('Expired jwt token')

        user_id = decoded.get('sub')
        return AuthCredentials(["authenticated"]), SimpleUser(user_id)


routes = [
    Mount('/api', routes=api_routes, name='api')
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(debug=True, routes=routes, middleware=middleware)


def run():
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")
