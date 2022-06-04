from pydantic import BaseModel


class RoomVoteCommand(BaseModel):
    vote: int
