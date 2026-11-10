import uuid
import httpx
from app.providers.base import BaseProvider
from app.schemas import ProviderResult

class GroqProvider(BaseProvider):
    """OpenAI-compatible GroqCloud adapter. Free-plan models/quotas can change."""
    def __init__(self, api_key: str, model: str, timeout: float = 45.0):
        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured")
        self.api_key, self.model, self.timeout = api_key, model, timeout

    async def generate(self, prompt, system_prompt=None, temperature=0.2, max_tokens=800):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages,
                      "temperature": temperature, "max_tokens": max_tokens},
            )
            response.raise_for_status()
            data = response.json()
        try:
            answer = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Groq returned an unexpected response shape") from exc
        return ProviderResult(text=answer or "", model=self.model,
                              request_id=data.get("id", str(uuid.uuid4())),
                              estimated_cost_usd=None)
