import enum

from pydantic import BaseModel


class ResponseType(enum.Enum):
    text = "text"
    sticker = "sticker"


class SimpleResponse(BaseModel):
    # by default we assume it's a text response
    type: ResponseType = ResponseType.text
    # it can be text or sticker id, depending on the message type
    data: str = None
