# File: travel_planner/tools/list_events.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class EventListRequest(BaseModel):
    location: str
    month: str

class EventListResponse(BaseModel):
    events: List[str]

@app.post("/", response_model=EventListResponse)
async def list_events(req: EventListRequest):
    # Mock response: return 3 sample events for June 2025 in major Japanese cities
    return EventListResponse(
        events=[
            "Gion Matsuri (Kyoto) - July 17-24, 2025 (floats parades and festivities)",
            "Sanno Matsuri (Tokyo) - Mid-June 2025 (processions around Hie Shrine)",
            "Aoi Matsuri (Kyoto) - May 15, 2025 (robed courtiers procession)"
        ]
    )