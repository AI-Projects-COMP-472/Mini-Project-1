"""Configuration for the Student Support AI assistant."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AssistantConfig:
    """Configuration values used by the assistant."""

    knowledge_base_path: Path = PROJECT_ROOT / "data" / "knowledge_base.csv"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    sentiment_model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    similarity_threshold: float = 0.35
    escalation_threshold: float = 0.90
    show_similarity_score: bool = True
