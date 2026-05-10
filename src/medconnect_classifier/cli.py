"""
CLI for MedConnect Patient Support Classifier.

Commands:
    classify   — classify a single message with a specific provider
    compare    — run the same message through all configured providers
    fallback   — classify using the fallback chain
    demo       — run all sample messages through mock provider

Usage:
    python -m medconnect_classifier.cli classify --provider mock --message "..."
    python -m medconnect_classifier.cli compare --message "..."
    python -m medconnect_classifier.cli demo
"""

import argparse
import json

from .mock_provider import classify_mock, SAMPLE_MESSAGES
from .providers import PROVIDER_MAP
from .fallback import classify_with_fallback
from .config import settings


def print_result(output: dict) -> None:
    """Pretty-print a classification result."""
    intent = output["result"]
    print(f"\n{'═' * 65}")
    print(f"  Provider  : {output['provider']}")
    print(f"  Latency   : {output['latency']}s")
    print(f"  Method    : {output.get('method', 'n/a')}")
    print(f"{'─' * 65}")
    print(f"  Category  : {intent.category:<20} Urgency : {intent.urgency}")
    print(f"  Sentiment : {intent.sentiment:<20} Dept    : {intent.department}")
    print(f"  Entities  : {intent.entities}")
    print(f"  Summary   : {intent.summary}")
    print(f"  Action    : {intent.recommended_action}")
    print(f"{'═' * 65}")


def cmd_classify(args) -> None:
    provider = args.provider.lower()
    message = args.message

    if provider == "mock":
        output = classify_mock(message)
    elif provider in PROVIDER_MAP:
        output = PROVIDER_MAP[provider](message)
    else:
        print(f"❌ Unknown provider '{provider}'. Choose from: mock, {', '.join(PROVIDER_MAP.keys())}")
        return

    print_result(output)


def cmd_compare(args) -> None:
    message = args.message
    available = settings.available_providers()

    if not available:
        print("ℹ️  No API keys found. Running mock only.\n")
        available = ["mock"]

    print(f"\n📋 Comparing {len(available)} provider(s) for:\n  \"{message[:80]}\"")

    for provider_name in available:
        try:
            fn = classify_mock if provider_name == "mock" else PROVIDER_MAP[provider_name]
            output = fn(message)
            print_result(output)
        except Exception as exc:
            print(f"\n⚠️  {provider_name} error: {exc}")

    print(f"\n✅ Comparison complete across {len(available)} provider(s).")


def cmd_fallback(args) -> None:
    output = classify_with_fallback(args.message)
    print(f"\n🔁 Fallback Result — Status: {output.get('status', 'n/a')}")
    print_result(output)


def cmd_demo(_args) -> None:
    print("\n🏥 MedConnect Demo — 5 Original Patient Messages\n")
    for i, message in enumerate(SAMPLE_MESSAGES, 1):
        print(f"\n[Message {i}] {message[:90]}...")
        output = classify_mock(message)
        print_result(output)
    print("\n✅ Demo complete. Add API keys to .env to run with real providers.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MedConnect Patient Support Classifier CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    # classify
    p_classify = subparsers.add_parser("classify", help="Classify with one provider")
    p_classify.add_argument("--provider", required=True, help="Provider name: mock | openai | anthropic | gemini")
    p_classify.add_argument("--message", required=True, help="Patient message to classify")
    p_classify.set_defaults(func=cmd_classify)

    # compare
    p_compare = subparsers.add_parser("compare", help="Compare all configured providers")
    p_compare.add_argument("--message", required=True, help="Patient message to classify")
    p_compare.set_defaults(func=cmd_compare)

    # fallback
    p_fallback = subparsers.add_parser("fallback", help="Classify using fallback chain")
    p_fallback.add_argument("--message", required=True, help="Patient message to classify")
    p_fallback.set_defaults(func=cmd_fallback)

    # demo
    p_demo = subparsers.add_parser("demo", help="Run demo with 5 sample patient messages")
    p_demo.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
