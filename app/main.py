from __future__ import annotations

import time
from typing import Literal, Optional, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Mini Text Service", version="1.0.0")


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    strategy: Optional[str] = "rules"


class ClassifyResponse(BaseModel):
    category: Literal["pergunta", "relato", "reclamacao"]
    confidence: float
    strategy: str
    elapsed_ms: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {
        "service": "mini-text-service",
        "version": "1.0.0",
        "endpoints": ["/health", "/info", "/classify", "/echo"],
    }


@app.post("/echo")
def echo(payload: dict):
    # Útil para testar requests/response e debug de rede
    return {"received": payload}


def classify_rules(text: str) -> Tuple[str, float]:
    t = text.strip().lower()

    # Heurísticas simples (não é um modelo)
    if "?" in t or t.startswith(("como ", "por que ", "pq ", "qual ", "quais ")):
        return "pergunta", 0.85

    if any(k in t for k in ["não funciona", "erro", "ruim", "problema", "insatisfeito", "reclama"]):
        return "reclamacao", 0.75

    return "relato", 0.60


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    start = time.time()

    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text must be non-empty")

    if req.strategy != "rules":
        raise HTTPException(status_code=400, detail="unsupported strategy")

    category, confidence = classify_rules(text)
    elapsed_ms = int((time.time() - start) * 1000)

    return ClassifyResponse(
        category=category,
        confidence=confidence,
        strategy=req.strategy,
        elapsed_ms=elapsed_ms,
    )
