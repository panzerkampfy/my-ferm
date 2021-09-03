from typing import Optional
from schemas import APIModel


class ProductZoneCreate(APIModel):
    product_id: int
    zone_id: int
    count: int


class ProductZone(ProductZoneCreate):
    id: int


class ProductZoneUpdate(APIModel):
    product_id: Optional[int]
    zone_id: Optional[int]
    count: Optional[int]

