from sqlalchemy.orm import Session

from app import models
from app.schemas import ProductCreate, OrderCreate


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


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()


def create_order(db: Session, order_data: OrderCreate):
    try:
        order = models.Order()

        db.add(order)
        db.flush()

        for item in order_data.items:
            product = get_product(db, item.product_id)

            if not product:
                raise ValueError(
                    f"Product {item.product_id} not found"
                )

            if product.stock < item.quantity:
                raise ValueError(
                    f"Insufficient stock for product {item.product_id}"
                )

            order_item = models.OrderItem(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )

            product.stock -= item.quantity

            db.add(order_item)

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise

def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()
