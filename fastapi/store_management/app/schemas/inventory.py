
from pydantic import BaseModel, Field


class InventoryAdjustment(BaseModel):
    product_id: int = Field(gt=0)
    quantity_change: int
    reason: str = Field(min_length=2, max_length=100)
