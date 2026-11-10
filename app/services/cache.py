import hashlib
import json
from app.core.config import Settings

class SemanticCache:
    """Redis exact-match response cache. Semantic vector matching is a future extension."""
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

    async def connect(self):
        if not self.settings.redis_url:
            return
        try:
            from redis.asyncio import Redis
            client = Redis.from_url(self.settings.redis_url, decode_responses=True,
                                    socket_connect_timeout=1, socket_timeout=1)
            await client.ping()
            self.client = client
        except Exception:
            self.client = None

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def make_key(self, prompt, task_type, system_prompt, provider="auto"):
        raw = json.dumps([prompt.strip(), task_type, system_prompt or "", provider], ensure_ascii=False)
        return "llmcache:v2:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def get(self, key):
        if not self.client:
            return None
        try:
            value = await self.client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None

    async def set(self, key, value):
        if not self.client:
            return
        try:
            await self.client.set(key, json.dumps(value), ex=self.settings.cache_ttl_seconds)
        except Exception:
            pass
