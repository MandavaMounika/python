
from pydantic import BaseModel, Field, ConfigDict


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    mobile_number: str = Field(
        pattern=r"^[6-9]\d{9}$",
        description="Enter a valid 10-digit Indian mobile number"
    )

    email: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    mobile_number: str
    email: str | None
    address: str | None
    model_config = ConfigDict(from_attributes=True)

class CustomerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: str | None = None
    address: str | None = None

