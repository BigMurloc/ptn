import datetime

import jwt
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from user.exceptions import UserDataValidationError, AuthenticationError
from user.repository.exceptions import ExistingUser
from user.user_service import get_user_service
from user.user_state import UserState


class Login(HTTPEndpoint):

    async def post(self, request):
        body = await request.json()
        service = get_user_service()

        try:
            username = body['login']
            password = body['password']
            service.login(username, password)
        except KeyError:
            return JSONResponse({'error': 'missing_attributes'}, status_code=400)
        except AuthenticationError:
            return JSONResponse({}, status_code=401)
        expiry = datetime.datetime.now() + datetime.timedelta(minutes=15)

        token = jwt.encode({'exp': expiry, 'sub': UserState().user.id}, 'secret',
                           algorithm='HS256')
        return JSONResponse({'token': token})


class Refresh(HTTPEndpoint):

    @requires('authenticated')
    async def post(self, request):
        if not request.user.is_authenticated:
            return JSONResponse({}, status_code=403)

        expiry = datetime.datetime.now() + datetime.timedelta(minutes=15)

        print(request.user.display_name)
        new_token = jwt.encode({'exp': expiry, 'sub': request.user.display_name},
                               'secret',
                               algorithm='HS256')
        return JSONResponse({'token': new_token})


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


class List(HTTPEndpoint):

    @requires('authenticated')
    async def get(self, request):
        service = get_user_service()
        usernames = service.find_usernames_by_username_like(request.query_params.get('filter'))
        return JSONResponse(usernames)


user_routes = [
    Route('/login', Login),
    Route('/register', Register),
    Route('/refresh', Refresh),
    Route('/list', List)
]
