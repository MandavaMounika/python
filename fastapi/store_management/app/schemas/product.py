from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class ProductCreate(BaseModel):
    product_code: str = Field(min_length=3, max_length=30)
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=5, ge=0)


class ProductResponse(BaseModel):
    id: int
    product_code: str
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    reorder_level: int
    model_config = ConfigDict(from_attributes=True)
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    reorder_level: int | None = Field(default=None, ge=0) 