"""Escalation policy for strongly negative student messages.

This module contains a simple rule that recommends contacting a human advisor
when the sentiment is negative with high confidence

"""

from __future__ import annotations


class EscalationPolicy:
    """Decides whether a message should be escalated to a human advisor."""

    def __init__(self, escalation_threshold: float) -> None:
        # Minimum negative confidence score required to escalate
        self.escalation_threshold = escalation_threshold

    def should_escalate(self, sentiment_label: str, sentiment_score: float) -> bool:
        """Return True when sentiment is strongly negative."""
        return sentiment_label == "NEGATIVE" and sentiment_score > self.escalation_threshold
