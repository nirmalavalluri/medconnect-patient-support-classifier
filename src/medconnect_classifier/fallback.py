"""
Multi-provider fallback classifier for MedConnect.

Tries providers in order and returns the first successful classification.
This mirrors the Polly resilience library pattern in .NET — retry with
exponential backoff and fallback to an alternative handler on failure.

Provider order: OpenAI → Anthropic → Gemini → Mock
"""

from .providers import PROVIDER_MAP
from .mock_provider import classify_mock
from .config import settings


def classify_with_fallback(message: str) -> dict:
    """Try each available provider in order; fall back to mock on all failures.

    Args:
        message: Raw patient support message to classify.

    Returns:
        dict with keys: provider, result (PatientIntent), latency, status, method.
    """
    available = settings.available_providers()

    if not available:
        print("  ℹ️  No API keys configured — using mock provider.")
        result = classify_mock(message)
        result["status"] = "✅ mock fallback"
        return result

    for provider_name in available:
        classify_fn = PROVIDER_MAP.get(provider_name)
        if not classify_fn:
            continue
        try:
            result = classify_fn(message)
            result["status"] = "✅ success"
            return result
        except Exception as exc:
            print(f"  ⚠️  {provider_name} failed: {exc}")
            continue

    # All real providers failed — fall back to mock
    print("  ⚠️  All providers failed — using mock fallback.")
    result = classify_mock(message)
    result["status"] = "⚠️  mock fallback (all providers failed)"
    return result
