
from sqlalchemy import Column, Integer, String
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    mobile_number = Column(
        String(10),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        nullable=True
    )

    address = Column(
        String(300),
        nullable=True
    )
