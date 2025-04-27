from pydantic import BaseModel
from datetime import datetime

class VacancyCreate(BaseModel):
    title: str
    description: str
    salary_from:int
    salary_to:int

class VacancyResponse(BaseModel):
    id: int
    title: str
    description: str
    salary_from:int
    salary_to:int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode=True