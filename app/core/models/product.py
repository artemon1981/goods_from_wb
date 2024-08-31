from typing import List, Dict

from sqlalchemy import Column, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Product(Base):
    __tablename__ = "product"

    nm_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    current_price: Mapped[float]
    sum_quantity: Mapped[int]
    quantity_by_sizes: Mapped[List[Dict]] = Column(JSON)

