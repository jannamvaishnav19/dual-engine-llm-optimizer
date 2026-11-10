import asyncio
import time
import secrets
from fastapi import APIRouter, Request, HTTPException, Depends, Header
from app.schemas import ChatRequest, ChatResponse, EvaluationResult
from app.services.router import ModelRouter
from app.services.judge import JudgeService
from app.providers.factory import ProviderFactory

router = APIRouter()
_model_router = ModelRouter()
_judge = JudgeService()

async def require_api_key(request: Request, x_api_key: str | None = Header(default=None)):
    settings = request.app.state.cache.settings
    if settings.app_env == "production":
        if not settings.api_key or not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
            raise HTTPException(status_code=401, detail="Valid X-API-Key header required")

@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
async def chat(payload: ChatRequest, request: Request):
    settings = request.app.state.cache.settings
    cache = request.app.state.cache
    started = time.perf_counter()
    provider_name = payload.provider or _model_router.choose(payload.prompt, payload.task_type)
    cache_key = await cache.make_key(payload.prompt, payload.task_type, payload.system_prompt, provider_name)
    cached = await cache.get(cache_key)
    if cached:
        return ChatResponse(**{**cached, "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                               "cached": True, "estimated_cost_usd": 0.0})
    provider = ProviderFactory.create(provider_name, settings)
    try:
        result = await provider.generate(payload.prompt, payload.system_prompt,
                                         payload.temperature, payload.max_tokens)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {type(exc).__name__}") from exc
    response = ChatResponse(
        answer=result.text, model=result.model, provider=provider_name,
        latency_ms=round((time.perf_counter() - started) * 1000, 2),
        cached=False, estimated_cost_usd=result.estimated_cost_usd, request_id=result.request_id,
    )
    await cache.set(cache_key, response.model_dump())
    if payload.evaluate:
        asyncio.create_task(_judge.evaluate(payload.prompt, result.text, provider_name, settings))
    return response

@router.post("/evaluate", response_model=EvaluationResult, dependencies=[Depends(require_api_key)])
async def evaluate(payload: ChatRequest, request: Request):
    settings = request.app.state.cache.settings
    provider_name = payload.provider or _model_router.choose(payload.prompt, payload.task_type)
    provider = ProviderFactory.create(provider_name, settings)
    try:
        result = await provider.generate(payload.prompt, payload.system_prompt,
                                         payload.temperature, payload.max_tokens)
        judge_result = await _judge.evaluate_now(payload.prompt, result.text, provider_name, settings)
        return EvaluationResult(**judge_result)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Evaluation failed: {type(exc).__name__}") from exc
