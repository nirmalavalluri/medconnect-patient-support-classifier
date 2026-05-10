# MedConnect Patient Support Classifier

A portfolio GenAI project that classifies patient support messages using multiple LLM providers — built by a .NET developer learning Agentic AI.

Compares **OpenAI**, **Anthropic Claude**, and **Google Gemini** on the same healthcare scenario using Pydantic structured outputs, latency tracking, and a production-style provider fallback pattern.

---

## The .NET Developer Perspective

Coming from an ASP.NET / C# background, every concept in this project maps directly to something I already knew:

| .NET / C# Concept | This Project's Equivalent |
|---|---|
| Strongly-typed C# DTO | `PatientIntent` Pydantic model |
| JSON deserialization to typed object | `responses.parse()` with schema validation |
| Polly retry / fallback policy | Multi-provider fallback chain |
| `IHttpClientFactory` with named clients | Provider SDK instances (OpenAI, Anthropic, Gemini) |
| `appsettings.json` + Azure Key Vault | `.env` + `python-dotenv` |
| Middleware / request pipeline | System prompt (LLM behavior control) |
| Strategy pattern | `PROVIDER_MAP` — each provider is a swappable strategy |

**The syntax changed. The engineering mindset did not.**

---

## Business Scenario

**MedConnect Health System** receives thousands of patient messages daily through its support portal. Before routing each message to the right department, the system must understand:

- What does the patient need? *(appointment / billing / prescription / emergency)*
- How urgent is it?
- What is the patient's emotional state?
- Which department should handle it?
- What should the support agent do first?

### Example Input

```
I am experiencing severe chest pain and shortness of breath and I cannot get
through to your emergency line. Please connect me to someone immediately.
This is very serious.
```

### Example Output

```json
{
  "category": "emergency",
  "urgency": "critical",
  "sentiment": "distressed",
  "department": "emergency",
  "entities": ["chest pain", "shortness of breath", "emergency line"],
  "summary": "Patient experiencing chest pain and shortness of breath cannot reach the emergency line.",
  "recommended_action": "Immediately connect to on-call emergency physician; follow critical escalation protocol."
}
```

---

## Architecture

```
Patient Message
      │
      ▼
 Provider Router
 ┌────────────────────────────────────┐
 │  OpenAI → Anthropic → Gemini       │  ← Fallback chain (like Polly in .NET)
 └────────────────────────────────────┘
      │
      ▼
 Pydantic Validation  ← Like C# DTO deserialization
      │
      ▼
 PatientIntent (structured result)
      │
      ▼
 Routing / Dashboard / CRM
```

---

## Project Structure

```
medconnect-patient-support-classifier/
├── src/
│   └── medconnect_classifier/
│       ├── schemas.py        # PatientIntent Pydantic model
│       ├── providers.py      # OpenAI, Anthropic, Gemini implementations
│       ├── fallback.py       # Multi-provider fallback chain
│       ├── mock_provider.py  # Demo without API keys
│       ├── prompts.py        # Prompt templates
│       ├── json_utils.py     # JSON sanitization helpers
│       ├── config.py         # API key configuration
│       └── cli.py            # Command-line interface
├── examples/
│   └── sample_messages.json  # 5 original synthetic patient messages
├── tests/
│   ├── test_schemas.py
│   └── test_json_utils.py
├── .env.example
├── requirements.txt
└── pyproject.toml
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nirmalavalluri/medconnect-patient-support-classifier.git
cd medconnect-patient-support-classifier
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Add your keys to `.env`:

```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Never commit `.env` to GitHub.

---

## Run the Project

### Demo mode — no API keys needed

```bash
python -m medconnect_classifier.cli demo
```

### Classify a single message

```bash
python -m medconnect_classifier.cli classify \
  --provider mock \
  --message "I have been waiting three weeks for my prescription refill."
```

### Compare all configured providers

```bash
python -m medconnect_classifier.cli compare \
  --message "I was charged twice for the same consultation. Please help."
```

### Run the fallback chain

```bash
python -m medconnect_classifier.cli fallback \
  --message "My child has a high fever and I cannot reach our pediatrician."
```

---

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Multi-provider LLM comparison | OpenAI, Anthropic Claude, Google Gemini |
| Native structured output | OpenAI `responses.parse()` with Pydantic |
| Prompt-based structured output | Anthropic JSON extraction + Pydantic validation |
| Schema-based structured output | Gemini `response_schema` |
| Provider fallback pattern | `fallback.py` — mirrors Polly in .NET |
| Schema validation | Pydantic `PatientIntent` model |
| Secure key management | `python-dotenv` — mirrors Azure Key Vault pattern |
| Mock provider | Demo without API keys — CI/CD friendly |

---

## Interview Talking Points

> I built a multi-provider AI patient support classifier for a healthcare scenario. The system compares OpenAI, Anthropic Claude, and Gemini for the same patient messages, measures latency, and returns schema-validated structured outputs using Pydantic. I implemented a provider fallback chain — similar to the Polly resilience pattern I used in my .NET APIs — so the system continues working if a provider fails. As a .NET developer, I found that the engineering patterns were identical; only the language and SDKs changed.

---

## Notes

- This is a learning and portfolio project — not a production medical system.
- All patient messages are synthetic and contain no real PII.
- Do not send real patient data, medical records, or personal health information to external LLM APIs.
- Model names and SDK APIs evolve — keep model names configurable via `.env`.

---

## License

MIT License
