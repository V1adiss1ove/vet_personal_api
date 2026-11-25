from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Pet(Base):
    name: Mapped[str] = mapped_column(String(128))
    species: Mapped[str] = mapped_column(String(128))
    breed: Mapped[str] = mapped_column(String(256))
    gender: Mapped[str]  # change type mb
    birth_date: Mapped[date | None]
    weight: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    notes: Mapped[str | None] = mapped_column(String(2000))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
    )
