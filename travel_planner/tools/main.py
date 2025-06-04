# File: travel_planner/tools/main.py

import uvicorn
from fastapi import FastAPI

# Import each tool’s FastAPI app
from .find_flights import app as find_flights_app
from .find_hotels import app as find_hotels_app
from .list_events import app as list_events_app
from .get_transport_options import app as transport_app

app = FastAPI()

# Mount each tool under /tools/<tool_name>
app.mount("/tools/find_flights", find_flights_app)
app.mount("/tools/find_hotels", find_hotels_app)
app.mount("/tools/list_events", list_events_app)
app.mount("/tools/get_transport_options", transport_app)

if __name__ == "__main__":
    uvicorn.run("travel_planner.tools.main:app", host="127.0.0.1", port=8002, reload=True)