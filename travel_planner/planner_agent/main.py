import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from shared_schema import PlanningRequest, PlanningResponse
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel planning assistant. Break down user goals into 3-5 specific planning steps."
                },
                {
                    "role": "user",
                    "content": f"My travel goal is: {request.goal}"
                }
            ]
        )
        raw_steps = response.choices[0].message.content
        steps = raw_steps.strip().split("\n")
        logging.info(f"[planner] Generated steps: {steps}")
        return PlanningResponse(steps=steps)
    except Exception as e:
        logging.error(f"[planner] Error while calling OpenAI: {e}")
        raise

@app.get("/status")
def status():
    return {"status": "ok", "agent": "planner"}