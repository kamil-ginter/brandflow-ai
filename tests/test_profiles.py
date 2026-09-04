from pathlib import Path

from brandflow.models import BrandProfile
from brandflow.profiles import delete_profile, load_profiles, save_profile


def test_profile_roundtrip(tmp_path: Path):
    store = tmp_path / "profiles.json"
    profile = BrandProfile(
        name="Northstar",
        audience="creators",
        tone="clear",
        offer="content workflows",
    )

    save_profile(store, profile)
    loaded = load_profiles(store)

    assert loaded["Northstar"] == profile

    delete_profile(store, "Northstar")
    assert "Northstar" not in load_profiles(store)
