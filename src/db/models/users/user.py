from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import AbstractModel


class User(AbstractModel):
    __tablename__ = "users__user"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)


__all__ = ("User",)
