from brandflow.models import BrandProfile, ContentRequest
from brandflow.prompting import build_brief


def test_brief_contains_brand_and_task_context():
    profile = BrandProfile(
        name="Northstar",
        audience="independent creators",
        tone="clear and practical",
        offer="content workflows",
        values="clarity",
        forbidden_phrases="guaranteed",
    )
    request = ContentRequest(
        content_type="Email",
        goal="Launch a toolkit",
        call_to_action="Explore the toolkit",
        extra_context="Keep it concise.",
    )

    brief = build_brief(profile, request)

    assert "Northstar" in brief
    assert "independent creators" in brief
    assert "Launch a toolkit" in brief
    assert "Explore the toolkit" in brief
    assert "guaranteed" in brief
