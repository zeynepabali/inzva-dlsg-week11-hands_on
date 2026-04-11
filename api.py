# api.py
import os
import time
import httpx
import mlflow

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="inzva-AI API",
    description="Privacy-first AI microservice for the inzva community",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str
    latency_ms: float

# Add this constant after the Pydantic models


SYSTEM_PROMPT = (
    "you are a snarky british helper, who gives funny responses while answering the user"
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Forward the user prompt to Ollama with the inzva system prompt."""

    start = time.time()

    payload = {
        "model": "qwen2.5:0.5b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": req.prompt},
        ],
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()

    latency_ms = (time.time() - start) * 1000
    answer = resp.json()["message"]["content"]

# Add this block INSIDE the chat() function, right before the return

    # ── MLflow Telemetry ──
    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment("inzva-ai-telemetry")

    with mlflow.start_run():
        mlflow.log_param("model", "qwen2.5:0.5b")
        mlflow.log_param("prompt", req.prompt[:200])
        mlflow.log_metric("latency_ms", latency_ms)
        mlflow.log_metric("response_length", len(answer))

    return ChatResponse(response=answer, latency_ms=round(latency_ms, 2))
