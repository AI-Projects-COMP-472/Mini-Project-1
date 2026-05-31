from pathlib import Path

from assistant.config import AssistantConfig
from assistant.escalation import EscalationPolicy
from assistant.support_assistant import SupportAssistant


class FakeSemanticSearch:
    def find_best_answer(self, message):
        return "Use the password reset portal.", "How do I reset my password?", 0.88


class FakeSentimentAnalyzer:
    def get_sentiment(self, message):
        return "NEGATIVE", 0.95


def test_support_assistant_processes_message_and_updates_stats():
    config = AssistantConfig(
        knowledge_base_path=Path(__file__).resolve().parents[1] / "data" / "knowledge_base.csv"
    )
    assistant = SupportAssistant(
        config=config,
        semantic_search=FakeSemanticSearch(),
        sentiment_analyzer=FakeSentimentAnalyzer(),
        escalation_policy=EscalationPolicy(escalation_threshold=0.90),
    )

    response = assistant.process_message("I cannot access my account")

    assert response.sentiment_label == "NEGATIVE"
    assert response.answer == "Use the password reset portal."
    assert response.should_escalate is True
    assert assistant.stats.total_questions == 1
    assert assistant.stats.sentiment_counts["NEGATIVE"] == 1


def test_support_assistant_rejects_empty_message():
    config = AssistantConfig(
        knowledge_base_path=Path(__file__).resolve().parents[1] / "data" / "knowledge_base.csv"
    )
    assistant = SupportAssistant(
        config=config,
        semantic_search=FakeSemanticSearch(),
        sentiment_analyzer=FakeSentimentAnalyzer(),
        escalation_policy=EscalationPolicy(escalation_threshold=0.90),
    )

    try:
        assistant.process_message("   ")
    except ValueError as error:
        assert "Message cannot be empty" in str(error)
    else:
        raise AssertionError("Expected ValueError for empty message.")
