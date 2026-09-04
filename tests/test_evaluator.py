from brandflow.evaluator import evaluate_brand_consistency
from brandflow.models import BrandProfile


def test_evaluator_rewards_brand_and_avoids_forbidden_phrase():
    profile = BrandProfile(
        name="Northstar",
        audience="independent creators",
        tone="clear",
        offer="content workflows",
        forbidden_phrases="guaranteed",
    )

    result = evaluate_brand_consistency(
        "Northstar helps independent creators build practical content workflows.",
        profile,
    )

    assert result.score == 100
    assert all(result.checks.values())


def test_evaluator_detects_forbidden_phrase():
    profile = BrandProfile(
        name="Northstar",
        audience="creators",
        tone="clear",
        offer="content workflows",
        forbidden_phrases="guaranteed",
    )

    result = evaluate_brand_consistency(
        "Northstar offers a guaranteed result for creators.",
        profile,
    )

    assert result.checks["forbidden_phrases_avoided"] is False
    assert result.score < 100
