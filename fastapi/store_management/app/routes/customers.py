
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer
from app.schemas.customers import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# 1. Register a new customer
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.mobile_number == customer_data.mobile_number
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer mobile number already registered"
        )

    new_customer = Customer(
        **customer_data.model_dump()
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# 2. Search customer by mobile number
@router.get(
    "/by-mobile/{mobile_number}",
    response_model=CustomerResponse
)
def get_customer_by_mobile(
    mobile_number: str,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.mobile_number == mobile_number
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# 3. Get all customers
@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


# 4. Get customer by ID
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# 5. Update customer details
@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first() 

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    update_data = customer_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer
