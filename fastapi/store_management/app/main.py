
from fastapi import FastAPI

from app.database import Base, engine

# Import all models before create_all
from app.models import (
    Product,
    Customer,
    InventoryTransaction,
    Sale,
    SaleItem,
    Payment
)

from app.routes.products import router as product_router
from app.routes.inventory import router as inventory_router
from app.routes.customers import router as customer_router
from app.routes.sales import router as sales_router


app = FastAPI(
    title="Store Management System"
)


Base.metadata.create_all(bind=engine)


app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(customer_router)
app.include_router(sales_router)


@app.get("/")
def home():
    return {
        "message": "Store Management API is running"
    }
