
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class SaleItemCreate(BaseModel):
    product_id: int = Field(gt=0)

    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    customer_id: int | None = None

    items: list[SaleItemCreate] = Field(
        min_length=1
    )

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2
    )

    payment_method: Literal[
        "cash",
        "upi",
        "card"
    ]


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    model_config = ConfigDict(from_attributes=True)


class PaymentResponse(BaseModel):
    id: int
    amount: Decimal
    method: str
    status: str
    transaction_reference: str | None

    model_config = ConfigDict(from_attributes=True)


class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: int | None
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str

    items: list[SaleItemResponse]
    payments: list[PaymentResponse]

    model_config = ConfigDict(from_attributes=True)
