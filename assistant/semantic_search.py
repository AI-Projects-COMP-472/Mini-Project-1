"""Semantic search using sentence embeddings and cosine similarity."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class SemanticSearch:
    """Finds the closest knowledge base answer for a user message."""

    def __init__(
        self,
        questions: List[str],
        answers: List[str],
        model_name: str,
        similarity_threshold: float,
        embedding_model=None,
        question_embeddings: np.ndarray | None = None,
    ) -> None:
        self.questions = questions
        self.answers = answers
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model or self.load_embedding_model(model_name)
        self.question_embeddings = (
            np.asarray(question_embeddings)
            if question_embeddings is not None
            else self.generate_embeddings(self.questions)
        )

    @staticmethod
    def load_embedding_model(model_name: str) -> SentenceTransformer:
        """
        Load the sentence-transformer model used for embeddings.

        Raises:
            RuntimeError: If the model cannot be loaded.
        """
        try:
            return SentenceTransformer(model_name)
        except Exception as error:
            raise RuntimeError(
                "Could not load the sentence embedding model. "
                "Check your internet connection on first run and confirm requirements are installed."
            ) from error

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Convert text into embeddings.

        Embeddings are arrays of numbers that represent the meaning of text.
        Questions with similar meaning should have similar embeddings.
        """
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return np.asarray(embeddings)

    def find_best_answer(self, message: str) -> Tuple[str, str, float]:
        """
        Retrieve the best answer using semantic search.

        Returns:
            A tuple containing the selected answer, matched question, and similarity score.
        """
        message_embedding = self.generate_embeddings([message])

        similarities = cosine_similarity(message_embedding, self.question_embeddings)[0]
        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])

        if best_score < self.similarity_threshold:
            fallback_answer = (
                "I could not find a confident answer for that question. "
                "Please contact Student Services or try rephrasing your question."
            )
            return fallback_answer, self.questions[best_index], best_score

        return self.answers[best_index], self.questions[best_index], best_score
