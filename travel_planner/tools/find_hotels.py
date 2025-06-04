# File: travel_planner/tools/find_hotels.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class HotelSearchRequest(BaseModel):
    location: str
    check_in: str
    check_out: str
    guests: int = 1

class HotelInfo(BaseModel):
    name: str
    address: str
    price_per_night: float
    rating: float

class HotelSearchResponse(BaseModel):
    hotels: List[HotelInfo]

@app.post("/", response_model=HotelSearchResponse)
async def find_hotels(req: HotelSearchRequest):
    # Mock response: return 3 sample hotels
    return HotelSearchResponse(
        hotels=[
            HotelInfo(
                name="Hotel Sakura (Shinjuku)",
                address="Shinjuku, Tokyo",
                price_per_night=150.0,
                rating=4.2
            ),
            HotelInfo(
                name="Kyoto Palace Inn",
                address="Gion, Kyoto",
                price_per_night=180.0,
                rating=4.5
            ),
            HotelInfo(
                name="Osaka Riverside Hotel",
                address="Kita, Osaka",
                price_per_night=120.0,
                rating=4.0
            )
        ]
    )