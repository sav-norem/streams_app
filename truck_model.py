from unicodedata import decimal
from redis_om import (Field, JsonModel)
from pydantic import PositiveInt
from typing import Optional, List

# the OM model for a food truck
class Vendor(JsonModel):
    cuisines: List[str] = Field(index=True)
    id: str = Field(index=False)
    name: str = Field(index=True, full_text_search=True)
    primary_cuisine: str = Field(index=True)
    vendor_lon: float
    vendor_lat: float