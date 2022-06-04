from pydantic import BaseModel
from pydantic.class_validators import Optional


class RoomPatchCommand(BaseModel):
    topic_id: Optional[int]
    password: Optional[str]
