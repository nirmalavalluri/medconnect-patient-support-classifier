"""
LLM provider implementations for MedConnect classifier.

Each provider follows the same interface — classify(message) -> PatientIntent.
This mirrors the Strategy pattern in .NET, where each provider is a concrete
implementation of a shared IClassificationProvider interface.

Groq is included but commented out — uncomment and add GROQ_API_KEY to enable.
"""

import json
import time
from typing import Optional

from .config import settings
from .prompts import SYSTEM_PROMPT, CLASSIFICATION_PROMPT_TEMPLATE
from .schemas import PatientIntent
from .json_utils import safe_parse_json


# ---------------------------------------------------------------------------
# OpenAI — native structured output via Responses API
# ---------------------------------------------------------------------------

def classify_openai(message: str) -> dict:
    """Classify using OpenAI with native Pydantic structured output.
    
    Uses responses.parse() which guarantees 100% schema compliance
    at the token generation level — no JSON parsing failures possible.
    """
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    start = time.time()

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": CLASSIFICATION_PROMPT_TEMPLATE.format(message=message),
            },
        ],
        text_format=PatientIntent,
    )

    latency = round(time.time() - start, 2)
    intent: PatientIntent = response.output_parsed

    return {
        "provider": "OpenAI (gpt-4o-mini)",
        "result": intent,
        "latency": latency,
        "method": "native structured output",
    }


# ---------------------------------------------------------------------------
# Anthropic Claude — prompt-based JSON + Pydantic validation
# ---------------------------------------------------------------------------

def classify_anthropic(message: str) -> dict:
    """Classify using Anthropic Claude with prompt-based JSON extraction.
    
    Claude does not support native structured output, so we instruct it
    to return raw JSON and validate with Pydantic — similar to deserializing
    a JSON string into a typed C# object after an HTTP call.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    start = time.time()

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        temperature=0.1,
        system=SYSTEM_PROMPT + "\nReturn ONLY raw JSON with no markdown or backticks.",
        messages=[
            {
                "role": "user",
                "content": CLASSIFICATION_PROMPT_TEMPLATE.format(message=message),
            }
        ],
    )

    latency = round(time.time() - start, 2)
    raw_text = response.content[0].text
    tokens = response.usage.input_tokens + response.usage.output_tokens

    parsed = safe_parse_json(raw_text)
    intent = PatientIntent(**parsed)

    return {
        "provider": "Anthropic (claude-haiku-4-5)",
        "result": intent,
        "latency": latency,
        "tokens": tokens,
        "method": "prompt-based JSON + Pydantic validation",
    }


# ---------------------------------------------------------------------------
# Google Gemini — native structured output via response_schema
# ---------------------------------------------------------------------------

def classify_gemini(message: str) -> dict:
    """Classify using Google Gemini with native structured output.
    
    Gemini supports response_schema for constrained generation,
    making it a reliable alternative to OpenAI for structured outputs.
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)
    start = time.time()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=CLASSIFICATION_PROMPT_TEMPLATE.format(message=message),
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=1024,
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=PatientIntent,
        ),
    )

    latency = round(time.time() - start, 2)
    parsed = json.loads(response.text)
    intent = PatientIntent(**parsed)

    return {
        "provider": "Google Gemini (gemini-2.0-flash)",
        "result": intent,
        "latency": latency,
        "method": "native structured output via response_schema",
    }


# ---------------------------------------------------------------------------
# Groq / Llama — commented out, uncomment to enable
# ---------------------------------------------------------------------------

# def classify_groq(message: str) -> dict:
#     """Classify using Groq Cloud (Llama 3.3 70B) with JSON mode.
#
#     Groq offers the fastest inference latency via custom hardware.
#     Uses json_object mode + prompt engineering for structured output.
#     """
#     from groq import Groq
#
#     client = Groq(api_key=settings.groq_api_key)
#     start = time.time()
#
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         temperature=0.1,
#         response_format={"type": "json_object"},
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT + "\nReturn ONLY raw JSON."},
#             {"role": "user", "content": CLASSIFICATION_PROMPT_TEMPLATE.format(message=message)},
#         ],
#     )
#
#     latency = round(time.time() - start, 2)
#     parsed = json.loads(response.choices[0].message.content)
#     intent = PatientIntent(**parsed)
#
#     return {
#         "provider": "Groq (llama-3.3-70b-versatile)",
#         "result": intent,
#         "latency": latency,
#         "method": "JSON mode + Pydantic validation",
#     }


PROVIDER_MAP = {
    "openai": classify_openai,
    "anthropic": classify_anthropic,
    "gemini": classify_gemini,
    # "groq": classify_groq,
}
