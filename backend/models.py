from pydantic import BaseModel, Field


class product(BaseModel):
    id: int 
    name: str 
    description: str
    price: float
    quantity: int 