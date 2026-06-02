from pathlib import Path

from assistant.config import AssistantConfig, PROJECT_ROOT
from assistant.escalation import EscalationPolicy
from assistant.support_assistant import SupportAssistant


class DummySemanticSearch:
    def find_best_answer(self, message):
        return "Test answer.", "Test question?", 0.99


class DummySentimentAnalyzer:
    def get_sentiment(self, message):
        return "NEUTRAL", 0.75


def test_default_knowledge_base_path_is_project_root_data_file():
    config = AssistantConfig()

    assert config.knowledge_base_path == PROJECT_ROOT / "data" / "knowledge_base.csv"
    assert config.knowledge_base_path.exists()


def test_support_assistant_loads_knowledge_base_even_when_cwd_changes(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    config = AssistantConfig()
    assistant = SupportAssistant(
        config=config,
        semantic_search=DummySemanticSearch(),
        sentiment_analyzer=DummySentimentAnalyzer(),
        escalation_policy=EscalationPolicy(escalation_threshold=0.90),
    )

    response = assistant.process_message("Hello")

    assert response.answer == "Test answer."
    assert assistant.stats.total_questions == 1
