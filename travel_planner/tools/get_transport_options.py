# File: travel_planner/tools/get_transport_options.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TransportRequest(BaseModel):
    location: str

class TransportResponse(BaseModel):
    modes: List[str]

@app.post("/", response_model=TransportResponse)
async def get_transport_options(req: TransportRequest):
    # Mock response: return sample transport modes for Japan
    return TransportResponse(
        modes=[
            "Shinkansen (bullet train) – connects major cities",
            "Local JR trains – regional coverage",
            "Subway systems – Tokyo, Osaka, Nagoya",
            "Buses – city and rural routes",
            "Taxi – everywhere, more expensive",
            "Rental bicycle – popular in Kyoto and smaller towns"
        ]
    )