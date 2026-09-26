from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal


app = FastAPI(
    title="E-Commerce Order Platform",
    version="1.0.0"
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
