"""
Configuration — loads API keys from environment variables.

Uses python-dotenv to load from a local .env file in development.
In production (Azure App Service, etc.), keys come from environment
variables — the same pattern as appsettings.json + Azure Key Vault in .NET.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")

    def available_providers(self) -> list[str]:
        providers = []
        if self.openai_api_key:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("anthropic")
        if self.gemini_api_key:
            providers.append("gemini")
        # if self.groq_api_key:
        #     providers.append("groq")
        return providers


settings = Settings()
