from pydantic import BaseModel
from datetime import datetime
from app.models.responses_model import ResponseStatus

class ResponseCreate(BaseModel):
    vacancy_id: int
    text: str

class ResponseUpdate(BaseModel):
    status: ResponseStatus

class ResponseOut(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    text: str
    status: ResponseStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode=True