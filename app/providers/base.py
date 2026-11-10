from abc import ABC, abstractmethod
from app.schemas import ProviderResult

class BaseProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str | None,
                       temperature: float, max_tokens: int) -> ProviderResult:
        raise NotImplementedError
