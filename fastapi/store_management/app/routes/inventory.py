
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, InventoryTransaction
from app.schemas.inventory import InventoryAdjustment

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post("/adjustments")
def adjust_inventory(
    adjustment: InventoryAdjustment,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == adjustment.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_stock = (
        product.stock_quantity
        + adjustment.quantity_change
    )

    if new_stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    try:
        product.stock_quantity = new_stock

        transaction = InventoryTransaction(
            product_id=product.id,
            quantity_change=adjustment.quantity_change,
            reason=adjustment.reason
        )

        db.add(transaction)
        db.commit()
        db.refresh(product)

    except Exception:
        db.rollback()
        raise

    return {
        "message": "Inventory updated successfully",
        "product_id": product.id,
        "product_code": product.product_code,
        "stock_quantity": product.stock_quantity
    }
@router.get("/low-stock")
def get_low_stock_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.stock_quantity <= Product.reorder_level
    ).all()

    return products