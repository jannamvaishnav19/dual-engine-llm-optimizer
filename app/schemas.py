from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4

ProviderName = Literal["gemini", "groq", "ollama"]

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    system_prompt: Optional[str] = Field(default=None, max_length=5000)
    task_type: Literal["auto", "fast", "long_context", "vision", "code", "reasoning"] = "auto"
    provider: Optional[ProviderName] = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=800, ge=1, le=8192)
    evaluate: bool = False

    @field_validator("prompt")
    @classmethod
    def prompt_not_blank(cls, value):
        if not value.strip():
            raise ValueError("prompt cannot be blank")
        return value

class ChatResponse(BaseModel):
    answer: str
    model: str
    provider: str
    latency_ms: float
    cached: bool
    estimated_cost_usd: Optional[float] = None
    request_id: str

class EvaluationResult(BaseModel):
    score: float
    verdict: str
    rationale: str
    judge_provider: str

class ProviderResult(BaseModel):
    text: str
    model: str
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    estimated_cost_usd: Optional[float] = None
