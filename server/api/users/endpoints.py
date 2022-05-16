from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from user.exceptions import UserDataValidationError
from user.repository.exceptions import ExistingUser
from user.user_service import get_user_service


class Login(HTTPEndpoint):

    async def get(self, request):
        return JSONResponse({'login': 'dunno'})


class Register(HTTPEndpoint):

    async def post(self, request):
        body = await request.json()
        service = get_user_service()

        try:
            username = body['login']
            password = body['password']
            service.register(username, password)
        except KeyError:
            return JSONResponse({'error': 'missing_attributes'}, status_code=400)
        except UserDataValidationError:
            return JSONResponse({'error': 'wrong_data'}, status_code=400)
        except ExistingUser:
            return JSONResponse({'error': 'existing_user'}, status_code=400)

        return JSONResponse({})


routes = [
    Route('/login', Login),
    Route('/register', Register)
]
