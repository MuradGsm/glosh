from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: int
    text: str

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    text: str
    is_read: bool

    class Config:
        orm_mode=True
