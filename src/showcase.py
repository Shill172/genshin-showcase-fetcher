"""Ties fetching and formatting together into one reusable entry point."""

from enka_client import fetch_showcase, fetch_character_metadata, fetch_localization, fetch_artifact_metadata
from resolver import format_character

# Using default values for now since no checkboxes/JS
DEFAULT_FIELDS = {"level", "constellation", "weapon", "artifact_set"}


def build_showcase_text(uid, fields=None):
    """Fetch a UID's showcase and return it as formatted text, one line per character."""
    if fields is None:
        fields = DEFAULT_FIELDS

    showcase = fetch_showcase(uid)
    chars = fetch_character_metadata()
    loc = fetch_localization()
    artifacts = fetch_artifact_metadata()

    lines = [
        format_character(char, chars, loc, artifacts, fields)
        for char in showcase["avatarInfoList"]
    ]
    return "\n".join(lines)