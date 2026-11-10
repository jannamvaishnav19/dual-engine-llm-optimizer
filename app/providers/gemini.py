import uuid
import httpx
from app.providers.base import BaseProvider
from app.schemas import ProviderResult

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: str, model: str, timeout: float = 45.0):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
        self.api_key, self.model, self.timeout = api_key, model, timeout

    async def generate(self, prompt, system_prompt=None, temperature=0.2, max_tokens=800):
        body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        if system_prompt:
            body["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, params={"key": self.api_key}, json=body)
            response.raise_for_status()
            data = response.json()
        try:
            text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Gemini returned an unexpected response shape") from exc
        return ProviderResult(text=text, model=self.model, request_id=str(uuid.uuid4()),
                              estimated_cost_usd=None)
