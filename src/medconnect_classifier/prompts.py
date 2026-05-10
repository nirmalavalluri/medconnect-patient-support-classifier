"""
Prompt templates for MedConnect Patient Support Classifier.

Keeping prompts in a dedicated module makes them easy to version,
A/B test, and swap — similar to resource files in .NET applications.
"""

SYSTEM_PROMPT = """You are an intelligent patient support assistant for MedConnect Health System.
Your role is to classify incoming patient messages accurately so they can be routed
to the correct department with the right priority level.

Always be thorough when extracting entities such as doctor names, medications,
appointment dates, insurance details, and monetary amounts.
Respond only with the structured data — no conversational filler."""

CLASSIFICATION_PROMPT_TEMPLATE = """Classify the following patient support message for MedConnect Health System.

Patient Message:
{message}

Return a structured classification with:
- category: one of appointment | billing | prescription | emergency | general_inquiry | complaint
- urgency: one of low | medium | high | critical
- sentiment: one of positive | neutral | concerned | distressed
- department: one of cardiology | general | billing | pharmacy | emergency | administration
- entities: list of key entities (doctor names, dates, medications, amounts, insurance info)
- summary: one sentence describing the core issue
- recommended_action: specific next step for the support agent

Return ONLY valid JSON. No markdown, no backticks, no explanation."""

JSON_SCHEMA = {
    "category": "appointment|billing|prescription|emergency|general_inquiry|complaint",
    "urgency": "low|medium|high|critical",
    "sentiment": "positive|neutral|concerned|distressed",
    "department": "cardiology|general|billing|pharmacy|emergency|administration",
    "entities": ["list", "of", "key", "entities"],
    "summary": "one sentence summary of the core issue",
    "recommended_action": "specific next step for the support agent",
}
