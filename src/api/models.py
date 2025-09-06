from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from .constants import PROVINCIAS_ARGENTINAS

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Courtfile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    case_number: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(
        Enum(
            *PROVINCIAS_ARGENTINAS,  
            name='provincias_argentinas_enum'
        ),
        nullable=False
    )
    court: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "case_number": self.case_number,
            "title": self.title,
            "description": self.description,
            "jurisdiction": self.jurisdiction,
            "court": self.court,
            "status": self.status,
        }

