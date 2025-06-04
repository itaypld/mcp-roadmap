

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from openai import OpenAI

load_dotenv()
client = OpenAI()
app = FastAPI()
logging.basicConfig(level=logging.INFO)

class AggregationRequest(BaseModel):
    results: List[Dict[str, str]]

class AggregationResponse(BaseModel):
    summary: str

@app.post("/aggregate", response_model=AggregationResponse)
async def aggregate(req: AggregationRequest):
    # Build prompt content
    content = "Here are the task results:\n" + "\n".join(
        f"Task: {r['task']}\nResult: {r['result']}" for r in req.results
    )
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that merges multiple task results into a coherent plan summary."},
            {"role": "user", "content": content}
        ]
    )
    summary = response.choices[0].message.content.strip()
    logging.info("[aggregator] Generated summary")
    return AggregationResponse(summary=summary)