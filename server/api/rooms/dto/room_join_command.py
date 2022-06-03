from pydantic import BaseModel


class RoomJoinCommand(BaseModel):
    password: str
