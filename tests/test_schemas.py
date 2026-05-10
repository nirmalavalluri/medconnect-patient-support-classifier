"""Tests for PatientIntent schema validation."""

import pytest
from medconnect_classifier.schemas import PatientIntent


def test_valid_patient_intent():
    intent = PatientIntent(
        category="emergency",
        urgency="critical",
        sentiment="distressed",
        department="emergency",
        entities=["chest pain", "shortness of breath"],
        summary="Patient experiencing chest pain needs immediate attention.",
        recommended_action="Connect to on-call emergency physician immediately.",
    )
    assert intent.category == "emergency"
    assert intent.urgency == "critical"


def test_invalid_category_raises():
    with pytest.raises(Exception):
        PatientIntent(
            category="unknown_category",
            urgency="low",
            sentiment="neutral",
            department="general",
            entities=[],
            summary="Test.",
            recommended_action="Test action.",
        )


def test_entities_is_list():
    intent = PatientIntent(
        category="billing",
        urgency="medium",
        sentiment="concerned",
        department="billing",
        entities=["$450", "BlueCross BlueShield"],
        summary="Billing dispute for $450.",
        recommended_action="Assign to billing team.",
    )
    assert isinstance(intent.entities, list)
    assert len(intent.entities) == 2


def test_all_categories_valid():
    valid_categories = ["appointment", "billing", "prescription", "emergency", "general_inquiry", "complaint"]
    for cat in valid_categories:
        intent = PatientIntent(
            category=cat,
            urgency="low",
            sentiment="neutral",
            department="general",
            entities=[],
            summary="Test summary.",
            recommended_action="Test action.",
        )
        assert intent.category == cat
