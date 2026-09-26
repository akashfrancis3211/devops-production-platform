from sqlalchemy.orm import Session

from app import models
from app.schemas import ProductCreate


def create_product(db: Session, product: ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()
