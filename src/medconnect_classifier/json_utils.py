"""
JSON utility helpers for prompt-based JSON extraction.

When providers like Anthropic return JSON wrapped in markdown fences,
these helpers strip the noise before parsing — equivalent to string
sanitization before deserialization in C#.
"""

import json
import re


def strip_markdown_fences(text: str) -> str:
    """Remove markdown code fences that some models add around JSON."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def safe_parse_json(text: str) -> dict:
    """Attempt to parse JSON, stripping markdown fences if needed.
    
    Raises ValueError with a clear message if parsing still fails.
    """
    cleaned = strip_markdown_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from provider response.\n"
            f"Original text: {text[:200]}\n"
            f"Error: {e}"
        )
