from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    species: str = Field(max_length=128)  # добавить min_length? сделать Enum?
    breed: str = Field(max_length=256)  # добавить min_length?
    gender: str  # сделать Enum?
    birth_date: date | None = Field(default=None, examples=["2026-11-24"])
    weight: Decimal | None = Field(gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)  # добавить min_length?


class PetRead(BaseModel):
    id: int
    name: str
    species: str
    breed: str
    gender: str
    birth_date: date | None
    weight: Decimal | None
    notes: str | None
    created_at: datetime


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    species: str | None = Field(default=None, max_length=128)
    breed: str | None = Field(default=None, max_length=256)
    gender: str | None = None  # change type mb
    birth_date: date | None = None
    weight: Decimal | None = Field(default=None, gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)
