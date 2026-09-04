from __future__ import annotations

import json
from pathlib import Path
from .models import BrandProfile


def load_profiles(path: Path) -> dict[str, BrandProfile]:
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    result: dict[str, BrandProfile] = {}
    for name, payload in data.items():
        try:
            result[name] = BrandProfile(**payload)
        except TypeError:
            continue
    return result


def save_profile(path: Path, profile: BrandProfile) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    profiles = load_profiles(path)
    profiles[profile.name] = profile
    path.write_text(
        json.dumps({name: p.as_dict() for name, p in profiles.items()}, indent=2),
        encoding="utf-8",
    )


def delete_profile(path: Path, name: str) -> None:
    profiles = load_profiles(path)
    profiles.pop(name, None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({n: p.as_dict() for n, p in profiles.items()}, indent=2),
        encoding="utf-8",
    )
