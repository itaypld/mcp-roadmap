import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from ..shared_schema import PlanningRequest, PlanningResponse
import logging

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("planner.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

@app.post("/plan", response_model=PlanningResponse)
async def generate_plan(request: PlanningRequest):
    logging.info(f"[planner] Received goal: {request.goal}")
    try:
        # Build user prompt, incorporating memory if available
        user_content = f"My travel goal is: {request.goal}"
        if request.memory_summary:
            user_content = f"Previous summary:\n{request.memory_summary}\n\n" + user_content

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the Planning Agent.\n"
                        "Available tools:\n"
                        "  • find_flights: takes JSON { origin: string, destination: string, depart_date: string, return_date: string (optional), passengers: int } and returns { offers: [{ airline: string, price: float, depart_time: string, arrive_time: string }] }.\n"
                        "  • find_hotels: takes JSON { location: string, check_in: string, check_out: string, guests: int } and returns { hotels: [{ name: string, address: string, price_per_night: float, rating: float }] }.\n"
                        "  • list_events: takes JSON { location: string, month: string } and returns { events: [string] }.\n"
                        "  • get_transport_options: takes JSON { location: string } and returns { modes: [string] }.\n\n"
                        "When given a user goal, return a JSON array of steps, each with:\n"
                        "  – “tool”: one of [“find_flights”, “find_hotels”, “list_events”, “get_transport_options”]\n"
                        "  – “input”: an object matching that tool’s schema\n\n"
                        "Return ONLY the JSON array of steps—no extra text."
                    )
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        )
        raw_steps = response.choices[0].message.content
        parsed_steps = json.loads(raw_steps)
        logging.info(f"[planner] Generated steps: {parsed_steps}")
        return PlanningResponse(steps=parsed_steps)
    except Exception as e:
        logging.error(f"[planner] Error while calling OpenAI: {e}")
        raise

@app.get("/status")
def status():
    return {"status": "ok", "agent": "planner"}