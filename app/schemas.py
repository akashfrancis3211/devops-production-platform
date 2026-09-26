from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int

    class Config:
        from_attributes = True
