import numpy as np

from assistant.semantic_search import SemanticSearch


class FakeEmbeddingModel:
    def encode(self, texts, convert_to_numpy=True):
        vectors = {
            "How do I reset my password?": [1.0, 0.0],
            "Where is the registrar office?": [0.0, 1.0],
            "password help": [1.0, 0.0],
            "unrelated": [0.1, 0.1],
        }
        return np.asarray([vectors[text] for text in texts])


def test_semantic_search_returns_best_answer():
    """Verify semantic search finds the best matching answer when similarity is high."""
    search = SemanticSearch(
        questions=["How do I reset my password?", "Where is the registrar office?"],
        answers=["Reset it online.", "Visit the administration building."],
        model_name="fake-model",
        similarity_threshold=0.35,
        embedding_model=FakeEmbeddingModel(),
    )

    answer, matched_question, score = search.find_best_answer("password help")

    assert answer == "Reset it online."
    assert matched_question == "How do I reset my password?"
    assert score == 1.0


def test_semantic_search_returns_fallback_when_confidence_is_low():
    """Verify semantic search returns fallback message when similarity is below threshold."""
    search = SemanticSearch(
        questions=["How do I reset my password?"],
        answers=["Reset it online."],
        model_name="fake-model",
        similarity_threshold=0.95,
        embedding_model=FakeEmbeddingModel(),
    )

    answer, matched_question, score = search.find_best_answer("unrelated")

    assert "could not find a confident answer" in answer
    assert matched_question == "How do I reset my password?"
    assert score < 0.95
