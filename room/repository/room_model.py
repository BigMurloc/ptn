class Room:
    def __init__(self, id, owner, hashed_password):
        self.id = id
        self.owner = owner
        self.password = hashed_password
