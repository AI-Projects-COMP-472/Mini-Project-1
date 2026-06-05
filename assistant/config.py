"""Configuration for the Student Support AI assistant.

This module centralizes default settings such as:
- knowledge-base path location
- Models names for embeddings and sentiment
- Thresholds for retrieval and escalation

"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Project root directory, used to build stable file paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class AssistantConfig:
    """Configuration values used by the assistant."""

    # Path of CSV file containing the knowledge base (Q&A pairs)
    knowledge_base_path: Path = PROJECT_ROOT / "data" / "knowledge_base.csv"
    
    # SentenceTransformers model from Hugging Face to embed text for semantic search
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Most popular model from Hugging Face to classify sentiment (positive|neutral|negative)
    sentiment_model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    # Minimum similarity required to accept a retrieved answer
    similarity_threshold: float = 0.35
    
    # Escalate to a human when negative sentiment confidence is above 90%
    escalation_threshold: float = 0.90
    
    # Print the similarity score
    show_similarity_score: bool = True
