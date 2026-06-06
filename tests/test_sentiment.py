from assistant.sentiment import SentimentAnalyzer


class FakeAnalyzer:
    def __call__(self, message):
        return [{"label": "LABEL_0", "score": 0.98}]


def test_sentiment_normalizes_hugging_face_label():
    """Verify sentiment analyzer converts Hugging Face label format to POSITIVE/NEUTRAL/NEGATIVE."""
    analyzer = SentimentAnalyzer("fake-model", analyzer=FakeAnalyzer())

    label, score = analyzer.get_sentiment("I am very frustrated")

    assert label == "NEGATIVE"
    assert score == 0.98


def test_unknown_sentiment_label_defaults_to_neutral():
    """Verify unknown sentiment labels are normalized to NEUTRAL as fallback."""
    assert SentimentAnalyzer.normalize_label("UNKNOWN") == "NEUTRAL"
