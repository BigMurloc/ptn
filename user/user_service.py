from repository.repository import Repository
from user.user_state import UserState


class UserService:

    def list_all(self, dirty_filter):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        clean_filter = dirty_filter.replace("--", "")  # -- is basically required to provide empty filter
        users = Repository().find_all()

        for user in users:
            if clean_filter in user.username:
                print(user.username)

    def delete(self, username):
        if not UserState().is_logged_in:
            raise RuntimeError('You are not authorized to do this operation')

        Repository().delete_by_username(username)
