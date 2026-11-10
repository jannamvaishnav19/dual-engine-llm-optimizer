from app.providers.gemini import GeminiProvider
from app.providers.groq import GroqProvider
from app.providers.ollama import OllamaProvider

class ProviderFactory:
    @staticmethod
    def create(name, settings):
        if name == "gemini":
            return GeminiProvider(settings.gemini_api_key, settings.gemini_model,
                                  settings.provider_timeout_seconds)
        if name == "groq":
            return GroqProvider(settings.groq_api_key, settings.groq_model,
                                settings.provider_timeout_seconds)
        if name == "ollama":
            return OllamaProvider(settings.ollama_base_url, settings.ollama_model,
                                  settings.provider_timeout_seconds)
        raise ValueError(f"Unsupported provider: {name}")
