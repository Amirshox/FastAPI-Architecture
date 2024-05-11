from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    def set_password(self, password):
        self.password = sha256.using().hash(password)

    def verify_password(self, password):
        return sha256.verify(password, self.password)


__all__ = ("User",)
