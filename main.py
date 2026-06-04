"""
COMP 472 Mini Project 1
Student Support AI Assistant with Sentiment Analysis and Semantic Search

Run:
    python main.py
"""

from __future__ import annotations

# assistant types (configuration, response DTO (Data Transfert Object), main assistant)
from assistant import AssistantConfig, AssistantResponse, SupportAssistant


def print_response(response: AssistantResponse, show_similarity_score: bool) -> None:
    """
    Print one assistant response using the required project output style.

    Args:
        response: Assistant response object.
        show_similarity_score: Whether to print the semantic match confidence.
    """
    print(f"Sentiment: {response.sentiment_label} ({response.sentiment_score:.2f})")

    # Escalate when strong negative sentiment is detected
    if response.should_escalate:
        print("Recommended escalation: Contact human advisor.")

    # Show semantic match confidence
    if show_similarity_score:
        print(f"Match confidence: {response.similarity_score:.2f}")

    print(f"Answer: {response.answer}")


def main() -> None:
    """
    Run the command-line conversation loop.

    The loop continues until the user types "quit".
    """
    # Load default configuration: Knowledge-base path, flags, models
    config = AssistantConfig()

    print("Loading Student Support AI...")

    # Initialize assistant
    try:
        assistant = SupportAssistant(config)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Startup error: {error}")
        return

    print("Welcome to Student Support AI")
    print("Type 'quit' to exit.")

    # conversation loop
    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("\nGoodbye.")
            
            # Print a breif summary before leaving
            print(assistant.get_conversation_summary())
            break

        if not user_input:
            print("Please enter a question or type 'quit' to exit.")
            continue

        # Process one user message and assistant response
        try:
            response = assistant.process_message(user_input)
            print_response(response, config.show_similarity_score)
        # Catch all exception to avoid breaking the interactive session
        except Exception as error:
            print(f"Sorry, something went wrong while processing your message: {error}")

# Allow running as a script: python main.py
if __name__ == "__main__":
    main()
