import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount

from server.api.endpoints import routes as api_routes

routes = [
    Mount('/api', routes=api_routes, name='api')
]

app = Starlette(debug=True, routes=routes)


def run():
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")
