from __future__ import annotations

import os
from abc import ABC, abstractmethod
import requests

from .models import BrandProfile, ContentRequest


class ContentProvider(ABC):
    @abstractmethod
    def generate(self, brief: str, profile: BrandProfile, request: ContentRequest) -> str:
        raise NotImplementedError


class DemoProvider(ContentProvider):
    """A deterministic provider so the project works without an API key."""

    def generate(self, brief: str, profile: BrandProfile, request: ContentRequest) -> str:
        kind = request.content_type.lower()

        if "email" in kind:
            return (
                f"Subject: {request.goal} — from {profile.name}\n\n"
                f"Hi,\n\n"
                f"{profile.name} is built for {profile.audience}. "
                f"We focus on {profile.offer.lower()} with a {profile.tone.lower()} approach.\n\n"
                f"{request.extra_context.strip() or 'The goal is to keep the message focused and useful.'}\n\n"
                f"{request.call_to_action}\n\n"
                f"— {profile.name}"
            )

        if "landing" in kind:
            return (
                f"# {request.goal}\n\n"
                f"## Built for {profile.audience}\n\n"
                f"{profile.name} helps with {profile.offer.lower()} while keeping the experience "
                f"{profile.tone.lower()} and focused.\n\n"
                f"{request.extra_context.strip() or 'Clear value, clear context and a direct next step.'}\n\n"
                f"**{request.call_to_action}**"
            )

        return (
            f"Form title: {request.goal}\n"
            f"Intro: {profile.name} created this form for {profile.audience}.\n"
            f"Field 1: Name\n"
            f"Field 2: Email\n"
            f"Field 3: What would you like help with?\n"
            f"Submit button: {request.call_to_action}"
        )


class OpenAICompatibleHTTPProvider(ContentProvider):
    def __init__(self) -> None:
        self.url = os.getenv("LLM_API_URL", "").strip()
        self.api_key = os.getenv("LLM_API_KEY", "").strip()
        self.model = os.getenv("LLM_MODEL", "").strip()

        if not self.url or not self.model:
            raise RuntimeError("LLM_API_URL and LLM_MODEL must be configured.")

    def generate(self, brief: str, profile: BrandProfile, request: ContentRequest) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You create concise, brand-consistent marketing content. "
                        "Never invent facts, metrics, testimonials or guarantees."
                    ),
                },
                {"role": "user", "content": brief},
            ],
            "temperature": 0.6,
        }

        response = requests.post(self.url, json=payload, headers=headers, timeout=45)
        response.raise_for_status()
        data = response.json()

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Unexpected response format from provider.") from exc


def get_provider() -> ContentProvider:
    name = os.getenv("BRANDFLOW_PROVIDER", "demo").strip().lower()
    if name == "demo":
        return DemoProvider()
    if name == "http":
        return OpenAICompatibleHTTPProvider()
    raise RuntimeError(f"Unknown provider: {name}")
