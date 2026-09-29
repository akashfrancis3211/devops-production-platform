from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal


app = FastAPI(
    title="E-Commerce Order Platform",
    version="1.1.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-api"
    }


@app.get("/")
def root():
    return {
        "application": "E-Commerce Order Platform",
        "version": "1.0.0"
    }


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)


@app.post(
    "/orders",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_order(db, order)

    except ValueError as error:
        message = str(error)

        if "not found" in message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


@app.get(
    "/orders",
    response_model=list[schemas.OrderResponse]
)
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.get(
    "/orders/{order_id}",
    response_model=schemas.OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = crud.get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )

    return order
