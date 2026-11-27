
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Sale
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.billing_services import create_sale


router = APIRouter(
    prefix="/sales",
    tags=["Billing"]
)


# 1. Create a bill
@router.post(
    "/",
    response_model=SaleResponse,
    status_code=201
)
def create_bill(
    sale_data: SaleCreate,
    db: Session = Depends(get_db)
):
    return create_sale(db, sale_data)


# 2. Get all sales
@router.get(
    "/",
    response_model=list[SaleResponse]
)
def get_sales(
    db: Session = Depends(get_db)
):
    return db.query(Sale).order_by(
        Sale.created_at.desc()
    ).all()


# 3. Get bill by ID
@router.get(
    "/{sale_id}",
    response_model=SaleResponse
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    sale = db.query(Sale).filter(
        Sale.id == sale_id
    ).first()

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale
