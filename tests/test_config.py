import pytest
from app.core.config import Settings

def test_production_requires_gateway_key():
    settings = Settings(app_env="production", api_key="", gemini_api_key="g", groq_api_key="r")
    with pytest.raises(RuntimeError):
        settings.validate_deployment()

def test_production_requires_both_provider_keys():
    settings = Settings(app_env="production", api_key="secret", gemini_api_key="g", groq_api_key="")
    with pytest.raises(RuntimeError):
        settings.validate_deployment()
