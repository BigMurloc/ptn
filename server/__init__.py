import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount

from server.api.endpoints import routes as api_routes

routes = [
    Mount('/api', routes=api_routes, name='api')
]

middleware = [
        Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]

app = Starlette(debug=True, routes=routes, middleware=middleware)


def run():
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")
