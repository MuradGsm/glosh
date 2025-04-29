from app.db.database import Base, pk_int
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Messages(Base):
    id: Mapped[pk_int]
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str]
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"{self.sender_id} is {self.receiver_id}"
