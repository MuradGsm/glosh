from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_employer: bool = True
    is_employee: bool = False

class UserResponse(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    email: EmailStr
    is_employer: bool
    is_employee: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True