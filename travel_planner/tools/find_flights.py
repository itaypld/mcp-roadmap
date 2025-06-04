# File: travel_planner/tools/find_flights.py

import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# In a real integration, you would load and use an actual flight‐search API key:
# SKYSCANNER_KEY = os.getenv("SKYSCANNER_API_KEY")

app = FastAPI()

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    depart_date: str
    return_date: Optional[str] = None
    passengers: int = 1

class FlightOffer(BaseModel):
    airline: str
    price: float
    depart_time: str
    arrive_time: str

class FlightSearchResponse(BaseModel):
    offers: List[FlightOffer]

@app.post("/", response_model=FlightSearchResponse)
async def find_flights(req: FlightSearchRequest):
    # Mock response: return 2 sample flights
    return FlightSearchResponse(
        offers=[
            FlightOffer(
                airline="Japan Airlines",
                price=850.00,
                depart_time=f"{req.depart_date}T08:00",
                arrive_time=f"{req.depart_date}T20:00"
            ),
            FlightOffer(
                airline="All Nippon Airways",
                price=820.00,
                depart_time=f"{req.depart_date}T09:30",
                arrive_time=f"{req.depart_date}T21:30"
            )
        ]
    )