"""
PatientIntent schema — structured output contract for MedConnect classifier.

Defines the exact fields the LLM must return for every patient message.
Using Pydantic ensures schema validation at the Python level — equivalent
to strongly-typed C# DTOs in .NET enterprise systems.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PatientIntent(BaseModel):
    """Structured classification output for a patient support message."""

    category: Literal[
        "appointment",
        "billing",
        "prescription",
        "emergency",
        "general_inquiry",
        "complaint",
    ] = Field(description="Primary intent category of the patient message")

    urgency: Literal["low", "medium", "high", "critical"] = Field(
        description="How urgently this message needs attention from the support team"
    )

    sentiment: Literal["positive", "neutral", "concerned", "distressed"] = Field(
        description="Patient's emotional tone in the message"
    )

    department: Literal[
        "cardiology",
        "general",
        "billing",
        "pharmacy",
        "emergency",
        "administration",
    ] = Field(description="Hospital department best suited to handle this message")

    entities: list[str] = Field(
        description="Key entities extracted: doctor names, dates, medications, amounts, insurance details"
    )

    summary: str = Field(
        description="One-sentence summary of the patient's core issue"
    )

    recommended_action: str = Field(
        description="Suggested next step for the support agent handling this message"
    )
