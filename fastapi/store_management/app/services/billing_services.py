
from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import (
    Product,
    Customer,
    Sale,
    SaleItem,
    Payment,
    InventoryTransaction
)
from app.schemas.sale import SaleCreate


# Tax percentage.
# Currently 0%. Configure the applicable tax rate
# before using this for real store billing.
TAX_RATE = Decimal("0.00")


def create_sale(db: Session, sale_data: SaleCreate):

    try:
        # 1. Check customer if customer_id is provided
        if sale_data.customer_id is not None:

            customer = db.query(Customer).filter(
                Customer.id == sale_data.customer_id
            ).first()

            if not customer:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found"
                )

        # 2. Prevent duplicate product IDs in one request
        product_ids = [
            item.product_id
            for item in sale_data.items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(
                status_code=400,
                detail="Do not repeat the same product. Combine its quantity."
            )

        subtotal = Decimal("0.00")
        sale_items = []

        # 3. Check products and calculate line totals
        for item in sale_data.items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).with_for_update().first()

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )

            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Insufficient stock for "
                        f"{product.name}. Available: "
                        f"{product.stock_quantity}"
                    )
                )

            unit_price = Decimal(product.price)

            line_total = (
                unit_price * item.quantity
            ).quantize(Decimal("0.01"))

            subtotal += line_total

            sale_items.append({
                "product": product,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "line_total": line_total
            })

        # 4. Calculate discount, tax and total
        discount = sale_data.discount_amount

        if discount > subtotal:
            raise HTTPException(
                status_code=400,
                detail="Discount cannot exceed subtotal"
            )

        taxable_amount = subtotal - discount

        tax_amount = (
            taxable_amount * TAX_RATE / Decimal("100")
        ).quantize(Decimal("0.01"))

        total_amount = taxable_amount + tax_amount

        # 5. Generate invoice number
        invoice_number = (
            "INV-" + uuid4().hex[:12].upper()
        )

        # 6. Create Sale record
        sale = Sale(
            invoice_number=invoice_number,
            customer_id=sale_data.customer_id,
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status="completed"
        )

        db.add(sale)
        db.flush()

        # 7. Create sale items and reduce stock
        for item in sale_items:

            product = item["product"]
            quantity = item["quantity"]

            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=item["unit_price"],
                line_total=item["line_total"]
            )

            db.add(sale_item)

            # Reduce product stock
            product.stock_quantity -= quantity

            # Record inventory movement
            inventory_record = InventoryTransaction(
                product_id=product.id,
                quantity_change=-quantity,
                reason="sale"
            )

            db.add(inventory_record)

        # 8. Record payment
        payment = Payment(
            sale_id=sale.id,
            amount=total_amount,
            method=sale_data.payment_method,
            status="successful"
        )

        db.add(payment)

        # 9. Save everything together
        db.commit()

        db.refresh(sale)

        return sale

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise
