from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import TIMESTAMP, ForeignKey, Numeric, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PetGender(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class SpeciesEnum(str, Enum):
    cat = "cat"
    dog = "dog"
    rabbit = "rabbit"
    bird = "bird"
    rodent = "rodent"
    other = "other"


class Pet(Base):
    name: Mapped[str] = mapped_column(String(128))
    species: Mapped[SpeciesEnum] = mapped_column(
        SQLEnum(SpeciesEnum, name="species_enum", native_enum=False)
    )
    breed: Mapped[str | None] = mapped_column(String(256))
    gender: Mapped[PetGender] = mapped_column(
        SQLEnum(PetGender, name="pet_gender", native_enum=False)
    )
    birth_date: Mapped[date | None]
    weight: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    notes: Mapped[str | None] = mapped_column(String(2000))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
    )
