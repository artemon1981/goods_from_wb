from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    nm_id: int
    current_price: float
    sum_quantity: int
    quantity_by_sizes: list


    class Config:
        from_attributes = True
