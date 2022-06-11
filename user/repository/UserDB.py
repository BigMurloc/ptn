from sqlalchemy import Column, Integer, Text

from util.database import Base


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(Text, nullable=False)
    username = Column(Text, nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
