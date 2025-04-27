from app.db.database import Base, pk_int
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Vacancy(Base):
    id: Mapped[pk_int]
    title: Mapped[str]
    description: Mapped[str]
    salary_from: Mapped[int] = mapped_column(nullable=True)
    salary_to: Mapped[int] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self):
        return f"Vacancy(id={self.id}, title={self.title})"
