"""Tests for JSON utility helpers."""

import pytest
from medconnect_classifier.json_utils import strip_markdown_fences, safe_parse_json


def test_strip_json_fence():
    text = "```json\n{\"key\": \"value\"}\n```"
    result = strip_markdown_fences(text)
    assert result == '{"key": "value"}'


def test_strip_plain_fence():
    text = "```\n{\"key\": \"value\"}\n```"
    result = strip_markdown_fences(text)
    assert result == '{"key": "value"}'


def test_no_fence_unchanged():
    text = '{"key": "value"}'
    result = strip_markdown_fences(text)
    assert result == '{"key": "value"}'


def test_safe_parse_valid_json():
    result = safe_parse_json('{"category": "billing"}')
    assert result["category"] == "billing"


def test_safe_parse_with_fence():
    text = '```json\n{"urgency": "high"}\n```'
    result = safe_parse_json(text)
    assert result["urgency"] == "high"


def test_safe_parse_invalid_raises():
    with pytest.raises(ValueError):
        safe_parse_json("not valid json at all")
