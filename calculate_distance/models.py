
from pydantic import BaseModel
from typing import List

class DistanceRequest(BaseModel):
    location_ids: List[str]

class LocationModel(BaseModel):
    name: str
    latitude: float
    longitude: float
