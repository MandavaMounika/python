
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    CheckConstraint,
    DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    reorder_level = Column(
        Integer,
        nullable=False,
        default=5
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    sale_items = relationship(
        "SaleItem",
        back_populates="product"
    )

    __table_args__ = (
        CheckConstraint("price > 0"),
        CheckConstraint("stock_quantity >= 0"),
        CheckConstraint("reorder_level >= 0")
    )
