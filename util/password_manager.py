import bcrypt


class PasswordManager:

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def verify_password(self, raw_password, hashed_password):
        return bcrypt.checkpw(raw_password.encode(self.encoding), hashed_password.encode(self.encoding))

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(self.encoding), bcrypt.gensalt())

    def encode(self, password):
        return password.encode(self.encoding)

    def decode(self, password):
        return password.decode(self.encoding)
