from unicodedata import decimal
from redis_om import (Field, JsonModel)
from pydantic import PositiveInt
from typing import Optional, List

class Vendor(JsonModel):
    cuisines: List[str] = Field(index=True)
    id: str = Field(index=False)
    name: str = Field(index=True, full_text_search=True)
    primary_cuisine: str = Field(index=True)
    restaurants_walkable: int = Field(index=True)
    vendor_lon: float
    vendor_lat: float