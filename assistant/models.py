"""Shared data models for assistant responses and statistics.

These dataclasses keep the assistant's internal data structured and easy to test:
- AssistantResponse: one processed user turn -> sentiment + retrieval result
- ConversationStats: lightweight counters for the current session

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AssistantResponse:
    """Represents the final response generated for one user message."""

    # Original user message cleaned
    user_message: str
    
    # Sentiment classification output
    sentiment_label: str
    sentiment_score: float
    
    # Retrieved or generated assistant answer + metadata
    answer: str
    matched_question: str
    similarity_score: float
    
    # Wheter the assistant recommends human assistance
    should_escalate: bool


@dataclass
class ConversationStats:
    """Tracks basic conversation statistics during one program run."""

    # total number of user questions processed
    total_questions: int = 0
    
    # Count of each sentiment label observed 
    sentiment_counts: Dict[str, int] = field(
        default_factory=lambda: {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    )

    def update(self, sentiment_label: str) -> None:
        """Update the statistics after one user message."""
        self.total_questions += 1
        self.sentiment_counts[sentiment_label] = self.sentiment_counts.get(sentiment_label, 0) + 1
