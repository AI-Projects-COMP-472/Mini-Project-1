"""Knowledge base loading and validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class KnowledgeBase:
    """Loads and validates the CSV question-answer knowledge base."""

    required_columns = {"question", "answer"}

    @classmethod
    def load(cls, file_path: Path) -> pd.DataFrame:
        """
        Load the knowledge base CSV file using pandas.

        Args:
            file_path: Path to the CSV file.

        Returns:
            A cleaned DataFrame with question and answer columns.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the CSV file is missing required columns or valid rows.
        """
        if not file_path.exists():
            raise FileNotFoundError(
                f"Could not find {file_path}. Make sure knowledge_base.csv is in the project folder."
            )

        data = pd.read_csv(file_path)

        if not cls.required_columns.issubset(data.columns):
            raise ValueError("knowledge_base.csv must contain exactly these required columns: question, answer")

        data = data.dropna(subset=["question", "answer"]).copy()
        data["question"] = data["question"].astype(str).str.strip()
        data["answer"] = data["answer"].astype(str).str.strip()
        data = data[(data["question"] != "") & (data["answer"] != "")]

        if data.empty:
            raise ValueError("knowledge_base.csv does not contain any valid question-answer rows.")

        return data.reset_index(drop=True)
