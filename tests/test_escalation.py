from assistant.escalation import EscalationPolicy


def test_escalation_when_negative_score_above_threshold():
    policy = EscalationPolicy(escalation_threshold=0.90)

    assert policy.should_escalate("NEGATIVE", 0.91) is True


def test_no_escalation_when_negative_score_at_threshold():
    policy = EscalationPolicy(escalation_threshold=0.90)

    assert policy.should_escalate("NEGATIVE", 0.90) is False


def test_no_escalation_for_non_negative_label():
    policy = EscalationPolicy(escalation_threshold=0.90)

    assert policy.should_escalate("NEUTRAL", 0.99) is False
    assert policy.should_escalate("POSITIVE", 0.99) is False
