import datetime

from jwt import ExpiredSignatureError
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from user.exceptions import UserDataValidationError, AuthenticationError
from user.repository.exceptions import ExistingUser
from user.user_service import get_user_service

import jwt

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

    async def post(self, request):
        if request.headers.get('authorization') is None:
            return JSONResponse({'error': 'authorization_header_required'}, status_code=400)

        token = request.headers.get('authorization')[4:]
        try:
            decoded_token = jwt.decode(token, 'secret', algorithms='HS256')
        except ExpiredSignatureError:
            return JSONResponse({}, status_code=403)

        print(decoded_token)

        expiry = datetime.datetime.now() + datetime.timedelta(minutes=15)

        new_token = jwt.encode({'exp': expiry, 'sub': decoded_token.get('sub')},
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


routes = [
    Route('/login', Login),
    Route('/register', Register),
    Route('/refresh', Refresh)
]
