from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class ClientCreate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    full_name: str = Field(max_length=255)
    phone: str = Field(max_length=30)
    address: str | None = Field(default=None, max_length=500)


class ClientRead(BaseModel):
    id: int
    email: EmailStr | None
    full_name: str
    phone: str
    address: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def check_required_fields_for_client(self):
        required = {"full_name", "phone"}
        for field in required & self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"Field '{field}' cannot be null")

        return self
