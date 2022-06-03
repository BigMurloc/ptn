class Room:
    def __init__(self, id, owner, name, hashed_password):
        self.id = id
        self.owner = owner
        self.name = name
        self.password = hashed_password
