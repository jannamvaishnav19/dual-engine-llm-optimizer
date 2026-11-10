from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.config import get_settings
from app.services.cache import SemanticCache

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    settings.validate_deployment()
    cache = SemanticCache(settings)
    await cache.connect()
    app.state.cache = cache
    yield
    await cache.close()

app = FastAPI(
    title="Dual-Engine LLM Judge & Cost-Latency Optimizer",
    description="Cloud-deployable dual-provider LLM gateway with Redis caching and cross-model evaluation.",
    version="1.1.0",
    lifespan=lifespan,
)
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"service": "Dual-Engine LLM Judge & Cost-Latency Optimizer",
            "docs": "/docs", "health": "/health"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
