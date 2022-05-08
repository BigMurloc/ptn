from user.repository.user_model import User


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class UserState(metaclass=SingletonMeta):
    user: User = None
    is_logged_in = False

    def is_authenticated(self):
        if self.user is None or self.is_logged_in is False:
            raise RuntimeError('You are not authenticated!')
