
from pydantic import BaseModel


class RoomCreateCommand(BaseModel):
    name: str
    password: str
