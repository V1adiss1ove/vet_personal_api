from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from app.models.pet import PetGender, SpeciesEnum


class PetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    species: Annotated[str, Field(max_length=12)] | SpeciesEnum
    breed: str | None = Field(default=None, min_length=2, max_length=256)
    gender: PetGender
    birth_date: date | None = Field(default=None, examples=["2026-11-24"])
    weight: Decimal | None = Field(default=None, gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, min_length=2, max_length=2000)


class PetRead(BaseModel):
    id: int
    name: str
    species: str | SpeciesEnum
    breed: str | None
    gender: PetGender
    birth_date: date | None
    weight: Decimal | None
    notes: str | None
    created_at: datetime


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    species: Annotated[str, Field(max_length=12)] | SpeciesEnum | None = None
    breed: str | None = Field(default=None, max_length=256)
    gender: PetGender | None = None
    birth_date: date | None = None
    weight: Decimal | None = Field(default=None, gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)
