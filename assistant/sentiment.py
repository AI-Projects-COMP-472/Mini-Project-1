"""Sentiment analysis for user messages."""

from __future__ import annotations

from typing import Tuple

from transformers import pipeline


class SentimentAnalyzer:
    """Detects positive, neutral, or negative sentiment from text."""

    label_mapping = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL",
        "LABEL_2": "POSITIVE",
    }

    def __init__(self, model_name: str, analyzer=None) -> None:
        self.analyzer = analyzer or self.load_sentiment_model(model_name)

    @staticmethod
    def load_sentiment_model(model_name: str):
        """
        Load the Hugging Face sentiment-analysis pipeline.

        Raises:
            RuntimeError: If the model cannot be loaded.
        """
        try:
            return pipeline("sentiment-analysis", model=model_name)
        except Exception as error:
            raise RuntimeError(
                "Could not load the sentiment model. "
                "Check your internet connection on first run and confirm requirements are installed."
            ) from error

    @classmethod
    def normalize_label(cls, label: str) -> str:
        """Normalize model labels into POSITIVE, NEUTRAL, or NEGATIVE."""
        normalized_label = cls.label_mapping.get(label.upper(), label.upper())

        if normalized_label not in {"POSITIVE", "NEUTRAL", "NEGATIVE"}:
            return "NEUTRAL"

        return normalized_label

    def get_sentiment(self, message: str) -> Tuple[str, float]:
        """
        Detect the sentiment of a user message.

        Returns:
            A tuple containing the sentiment label and confidence score.
        """
        result = self.analyzer(message)[0]
        label = self.normalize_label(str(result["label"]))
        score = float(result["score"])
        return label, score
