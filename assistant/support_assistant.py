"""Coordinator for the Student Support AI assistant.

This module connects together the main assitant components:
- knowledge-base loading
- Semantic retrieval -> embeddings + similarity
- Sentiment analysis -> classifier
- Escalating policy -> rule-based
- Conversation history + basic session stats


"""

from __future__ import annotations

from typing import List

from assistant.config import AssistantConfig
from assistant.escalation import EscalationPolicy
from assistant.knowledge_base import KnowledgeBase
from assistant.models import AssistantResponse, ConversationStats
from assistant.semantic_search import SemanticSearch
from assistant.sentiment import SentimentAnalyzer


class SupportAssistant:
    """
    Student support assistant.

    This class separates the assistant logic from the command-line interface.
    That makes the project easier to reuse later in a GUI, web app, or API.
    """

    def __init__(
        self,
        config: AssistantConfig,
        semantic_search: SemanticSearch | None = None,
        sentiment_analyzer: SentimentAnalyzer | None = None,
        escalation_policy: EscalationPolicy | None = None,
    ) -> None:
        
        # Store configuration (path, models names, thresholds, flags)
        self.config = config

        # Load the knowledge base -> expects question and answer columns
        self.knowledge_base = KnowledgeBase.load(config.knowledge_base_path)
        self.questions = self.knowledge_base["question"].tolist()
        self.answers = self.knowledge_base["answer"].tolist()

        # Create default components unless dependency-injected 
        self.semantic_search = semantic_search or SemanticSearch(
            questions=self.questions,
            answers=self.answers,
            model_name=config.embedding_model_name,
            similarity_threshold=config.similarity_threshold,
        )
        self.sentiment_analyzer = sentiment_analyzer or SentimentAnalyzer(config.sentiment_model_name)
        self.escalation_policy = escalation_policy or EscalationPolicy(config.escalation_threshold)

        # Track conversation turns and aggregate session stats 
        self.conversation_history: List[AssistantResponse] = []
        self.stats = ConversationStats()

    def process_message(self, message: str) -> AssistantResponse:
        """
        Process one user message and return the assistant result.

        Args:
            message: User input.

        Returns:
            AssistantResponse containing sentiment, answer, similarity, and escalation information.
        """
        cleaned_message = message.strip()
        
        # Basic validation before sending text to models
        if not cleaned_message:
            raise ValueError("Message cannot be empty.")

        # Sentiment detection
        sentiment_label, sentiment_score = self.sentiment_analyzer.get_sentiment(cleaned_message)
        
        # Retrieve the closest knowledge-base entryvia semantic similarity
        answer, matched_question, similarity_score = self.semantic_search.find_best_answer(cleaned_message)
        
        # Decide whether to recommend escalation
        should_escalate = self.escalation_policy.should_escalate(sentiment_label, sentiment_score)

        # Keep track of conversation state for summaries and analytics
        response = AssistantResponse(
            user_message=cleaned_message,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
            answer=answer,
            matched_question=matched_question,
            similarity_score=similarity_score,
            should_escalate=should_escalate,
        )

        self.conversation_history.append(response)
        self.stats.update(sentiment_label)

        return response

    def get_conversation_summary(self) -> str:
        """
        Create a short summary of the current conversation session.

        Returns:
            A printable conversation summary.
        """
        return (
            f"Questions asked: {self.stats.total_questions}\n"
            f"Positive messages: {self.stats.sentiment_counts.get('POSITIVE', 0)}\n"
            f"Neutral messages: {self.stats.sentiment_counts.get('NEUTRAL', 0)}\n"
            f"Negative messages: {self.stats.sentiment_counts.get('NEGATIVE', 0)}"
        )
