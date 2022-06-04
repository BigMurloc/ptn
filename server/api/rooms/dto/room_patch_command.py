from pydantic import BaseModel
from pydantic.class_validators import Optional


class RoomPatchCommand(BaseModel):
    topic: Optional[str]
    password: Optional[str]
