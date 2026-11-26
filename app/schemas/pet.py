from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.pet import PetGender, SpeciesEnum


class PetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    species: SpeciesEnum
    breed: str | None = Field(default=None, min_length=3, max_length=256)
    gender: PetGender
    birth_date: date | None = Field(default=None, examples=["2026-11-24"])
    weight: Decimal | None = Field(default=None, gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, min_length=2, max_length=2000)

    @field_validator("birth_date")
    @classmethod
    def check_date(cls, v: date):
        if v > date.today():
            raise ValueError("Некорретная дата")
        return v


class PetRead(BaseModel):
    id: int
    name: str
    species: SpeciesEnum
    breed: str | None
    gender: PetGender
    birth_date: date | None
    weight: Decimal | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    species: SpeciesEnum | None = None
    breed: str | None = Field(default=None, min_length=3, max_length=256)
    gender: PetGender | None = None
    birth_date: date | None = None
    weight: Decimal | None = Field(default=None, gt=0, max_digits=5, decimal_places=2)
    notes: str | None = Field(default=None, min_length=2, max_length=2000)
