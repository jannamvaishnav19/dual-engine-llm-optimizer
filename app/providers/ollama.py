import uuid
import httpx
from app.providers.base import BaseProvider
from app.schemas import ProviderResult

class OllamaProvider(BaseProvider):
    def __init__(self, base_url: str, model: str, timeout: float = 45.0):
        self.base_url, self.model, self.timeout = base_url.rstrip("/"), model, timeout

    async def generate(self, prompt, system_prompt=None, temperature=0.2, max_tokens=800):
        body = {"model": self.model, "prompt": prompt, "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens}}
        if system_prompt:
            body["system"] = system_prompt
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=body)
            response.raise_for_status()
            data = response.json()
        return ProviderResult(text=data.get("response", ""), model=self.model,
                              request_id=str(uuid.uuid4()), estimated_cost_usd=0.0)
