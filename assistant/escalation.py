"""Escalation policy for strongly negative student messages."""

from __future__ import annotations


class EscalationPolicy:
    """Decides whether a message should be escalated to a human advisor."""

    def __init__(self, escalation_threshold: float) -> None:
        self.escalation_threshold = escalation_threshold

    def should_escalate(self, sentiment_label: str, sentiment_score: float) -> bool:
        """Return True when sentiment is strongly negative."""
        return sentiment_label == "NEGATIVE" and sentiment_score > self.escalation_threshold
