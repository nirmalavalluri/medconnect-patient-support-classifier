"""
Mock provider — returns realistic classifications without real API calls.

Useful for CI/CD pipelines, demos, and local development without API keys.
Each message below is an original synthetic patient scenario — not derived
from any course material or third-party dataset.
"""

import time
from .schemas import PatientIntent

# ---------------------------------------------------------------------------
# Original synthetic patient messages for demo and testing
# ---------------------------------------------------------------------------

SAMPLE_MESSAGES = [
    "I have been trying to reschedule my cardiology appointment with Dr. Sarah Mitchell "
    "for two weeks. My original appointment was March 15th and nobody has called me back. "
    "I have a follow-up stress test that cannot be delayed any further.",

    "I was charged $450 for a routine consultation that my BlueCross BlueShield insurance "
    "should have fully covered. This is the third billing error in six months and I am "
    "extremely frustrated. I need this resolved before my next visit.",

    "My doctor prescribed Metformin 500mg last Tuesday but the pharmacy says the "
    "prescription is not on file. I am diabetic and have been without my medication "
    "for three days now. Please help urgently.",

    "I am experiencing severe chest pain and shortness of breath and I cannot get "
    "through to your emergency line. Please connect me to someone immediately. "
    "This is very serious.",

    "Could you let me know what documents I need to bring for my MRI scan scheduled "
    "for next Friday? This is my first time having this procedure and I want to "
    "make sure I am fully prepared.",
]

# Pre-built mock responses matching each sample message
MOCK_RESPONSES = [
    PatientIntent(
        category="appointment",
        urgency="high",
        sentiment="concerned",
        department="cardiology",
        entities=["Dr. Sarah Mitchell", "March 15th", "stress test", "two weeks"],
        summary="Patient cannot reschedule a delayed cardiology follow-up appointment with Dr. Sarah Mitchell.",
        recommended_action="Escalate to cardiology scheduling team immediately; prioritize callback within 2 hours given pending stress test.",
    ),
    PatientIntent(
        category="billing",
        urgency="medium",
        sentiment="distressed",
        department="billing",
        entities=["$450", "BlueCross BlueShield", "routine consultation", "third billing error"],
        summary="Patient disputes a $450 charge that their BlueCross BlueShield insurance should have covered.",
        recommended_action="Assign to billing dispute team; review insurance claims history for this patient; contact within 24 hours.",
    ),
    PatientIntent(
        category="prescription",
        urgency="critical",
        sentiment="distressed",
        department="pharmacy",
        entities=["Metformin 500mg", "Tuesday", "three days", "diabetic"],
        summary="Diabetic patient has been without prescribed Metformin for three days due to a missing prescription.",
        recommended_action="Contact prescribing physician immediately to resend prescription; arrange emergency supply if needed.",
    ),
    PatientIntent(
        category="emergency",
        urgency="critical",
        sentiment="distressed",
        department="emergency",
        entities=["chest pain", "shortness of breath", "emergency line"],
        summary="Patient is experiencing chest pain and shortness of breath and cannot reach the emergency line.",
        recommended_action="Immediately connect to on-call emergency physician; follow critical escalation protocol.",
    ),
    PatientIntent(
        category="general_inquiry",
        urgency="low",
        sentiment="neutral",
        department="administration",
        entities=["MRI scan", "next Friday", "first time"],
        summary="Patient is asking what documents to bring for their upcoming MRI scan.",
        recommended_action="Send MRI preparation checklist via email; confirm appointment details and any dietary restrictions.",
    ),
]


def classify_mock(message: str) -> dict:
    """Return a mock classification based on keyword matching.
    
    Falls back to the first mock response for unrecognised messages.
    """
    time.sleep(0.1)  # Simulate minimal latency

    message_lower = message.lower()

    if any(word in message_lower for word in ["chest pain", "shortness", "emergency", "serious"]):
        intent = MOCK_RESPONSES[3]
    elif any(word in message_lower for word in ["metformin", "prescription", "pharmacy", "medication", "diabetic"]):
        intent = MOCK_RESPONSES[2]
    elif any(word in message_lower for word in ["charged", "billing", "insurance", "payment", "$"]):
        intent = MOCK_RESPONSES[1]
    elif any(word in message_lower for word in ["appointment", "reschedule", "cardiology", "dr.", "doctor"]):
        intent = MOCK_RESPONSES[0]
    else:
        intent = MOCK_RESPONSES[4]

    return {
        "provider": "Mock (no API key required)",
        "result": intent,
        "latency": 0.1,
        "method": "keyword-based mock classification",
    }
