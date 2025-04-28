from app.db.database import Base, pk_int
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from enum import Enum as EnumPy

class ResponseStatus(EnumPy):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Response(Base):
    id: Mapped[pk_int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancys.id'))
    text: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[ResponseStatus] = mapped_column(
        Enum(ResponseStatus, name="response_status_enum"), 
        default=ResponseStatus.pending)

    def __repr__(self):
        return f'User is {self.user_id} in vanacy {self.vacancy_id}'
    
