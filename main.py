"""
COMP 472 Mini Project 1
Student Support AI Assistant with Sentiment Analysis and Semantic Search

Run:
    python main.py
"""

from __future__ import annotations

from assistant import AssistantConfig, AssistantResponse, SupportAssistant


def print_response(response: AssistantResponse, show_similarity_score: bool) -> None:
    """
    Print one assistant response using the required project output style.

    Args:
        response: Assistant response object.
        show_similarity_score: Whether to print the semantic match confidence.
    """
    print(f"Sentiment: {response.sentiment_label} ({response.sentiment_score:.2f})")

    if response.should_escalate:
        print("Recommended escalation: Contact human advisor.")

    if show_similarity_score:
        print(f"Match confidence: {response.similarity_score:.2f}")

    print(f"Answer: {response.answer}")


def main() -> None:
    """
    Run the command-line conversation loop.

    The loop continues until the user types "quit".
    """
    config = AssistantConfig()

    print("Loading Student Support AI...")

    try:
        assistant = SupportAssistant(config)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Startup error: {error}")
        return

    print("Welcome to Student Support AI")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("\nGoodbye.")
            print(assistant.get_conversation_summary())
            break

        if not user_input:
            print("Please enter a question or type 'quit' to exit.")
            continue

        try:
            response = assistant.process_message(user_input)
            print_response(response, config.show_similarity_score)
        except Exception as error:
            print(f"Sorry, something went wrong while processing your message: {error}")


if __name__ == "__main__":
    main()
