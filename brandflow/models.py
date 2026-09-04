from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BrandProfile:
    name: str
    audience: str
    tone: str
    offer: str
    values: str = ""
    forbidden_phrases: str = ""

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ContentRequest:
    content_type: str
    goal: str
    call_to_action: str
    extra_context: str = ""
