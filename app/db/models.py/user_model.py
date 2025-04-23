from app.db.database import Base, pk_int
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

class User(Base):
    id: Mapped[pk_int]
    phone_number: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

    is_employer: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_employee: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"