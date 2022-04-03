import uuid


class Room:
    def __init__(self, owner, hashed_password, given_uuid = uuid.uuid4(),):
        self.uuid = given_uuid
        self.owner = owner
        self.password = hashed_password
