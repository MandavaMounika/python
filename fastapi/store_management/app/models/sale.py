
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_number = Column(
        String(40),
        unique=True,
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    discount_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    tax_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="completed"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="sale",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("subtotal >= 0"),
        CheckConstraint("discount_amount >= 0"),
        CheckConstraint("tax_amount >= 0"),
        CheckConstraint("total_amount >= 0"),
    )
