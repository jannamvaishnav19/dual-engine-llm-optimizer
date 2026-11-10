import pytest
from app.services.cache import SemanticCache
from app.core.config import Settings

@pytest.mark.asyncio
async def test_cache_key_is_deterministic_and_provider_specific():
    cache = SemanticCache(Settings())
    a = await cache.make_key("hello", "auto", None, "gemini")
    b = await cache.make_key("hello", "auto", None, "gemini")
    c = await cache.make_key("hello", "auto", None, "groq")
    assert a == b
    assert a != c

@pytest.mark.asyncio
async def test_cache_degrades_without_redis():
    cache = SemanticCache(Settings())
    assert await cache.get("missing") is None
    await cache.set("key", {"answer": "value"})
