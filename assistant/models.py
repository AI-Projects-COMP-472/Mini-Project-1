"""Shared data models for assistant responses and statistics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AssistantResponse:
    """Represents the final response generated for one user message."""

    user_message: str
    sentiment_label: str
    sentiment_score: float
    answer: str
    matched_question: str
    similarity_score: float
    should_escalate: bool


@dataclass
class ConversationStats:
    """Tracks basic conversation statistics during one program run."""

    total_questions: int = 0
    sentiment_counts: Dict[str, int] = field(
        default_factory=lambda: {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    )

    def update(self, sentiment_label: str) -> None:
        """Update the statistics after one user message."""
        self.total_questions += 1
        self.sentiment_counts[sentiment_label] = self.sentiment_counts.get(sentiment_label, 0) + 1
