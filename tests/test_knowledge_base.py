from pathlib import Path

import pandas as pd

from assistant.knowledge_base import KnowledgeBase


def test_knowledge_base_has_required_columns_and_rows():
    """Verify knowledge base CSV has required columns, enough rows, and no null values."""
    path = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.csv"
    data = KnowledgeBase.load(path)

    assert "question" in data.columns
    assert "answer" in data.columns
    assert len(data) >= 10
    assert data["question"].notna().all()
    assert data["answer"].notna().all()


def test_knowledge_base_rejects_missing_columns(tmp_path):
    """Verify knowledge base loader raises error when required 'answer' column is missing."""
    path = tmp_path / "bad_knowledge_base.csv"
    pd.DataFrame({"question": ["How do I register?"]}).to_csv(path, index=False)

    try:
        KnowledgeBase.load(path)
    except ValueError as error:
        assert "question, answer" in str(error)
    else:
        raise AssertionError("Expected ValueError for missing answer column.")
