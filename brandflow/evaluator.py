from dataclasses import dataclass
from .models import BrandProfile


@dataclass(frozen=True)
class EvaluationResult:
    score: int
    checks: dict[str, bool]


def _split_forbidden(raw: str) -> list[str]:
    return [
        item.strip().lower()
        for item in raw.replace("\n", ",").split(",")
        if item.strip()
    ]


def evaluate_brand_consistency(text: str, profile: BrandProfile) -> EvaluationResult:
    """
    Lightweight deterministic checks.
    This is not pretending to be a semantic quality score; it is only a quick signal.
    """
    haystack = text.lower()

    brand_present = profile.name.lower() in haystack

    audience_words = [
        w.strip(".,:;!?()[]{}").lower()
        for w in profile.audience.split()
        if len(w.strip(".,:;!?()[]{}")) >= 4
    ]
    audience_signal = any(word in haystack for word in audience_words) if audience_words else False

    forbidden = _split_forbidden(profile.forbidden_phrases)
    avoids_forbidden = not any(item in haystack for item in forbidden)

    checks = {
        "brand_name_present": brand_present,
        "audience_signal_present": audience_signal,
        "forbidden_phrases_avoided": avoids_forbidden,
    }

    weights = {
        "brand_name_present": 35,
        "audience_signal_present": 25,
        "forbidden_phrases_avoided": 40,
    }
    score = sum(weights[k] for k, ok in checks.items() if ok)

    return EvaluationResult(score=score, checks=checks)
