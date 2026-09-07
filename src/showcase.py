"""Ties fetching and formatting together into one reusable entry point."""

from src.enka_client import fetch_showcase, fetch_character_metadata, fetch_localization, fetch_artifact_metadata
from src.resolver import format_character, format_character_line

# Using default values for now since no checkboxes/JS
DEFAULT_FIELDS = {
    "level", 
    "constellation", 
    "weapon", 
    "artifact_set",
   "friendship",
   "talents",
   "hp",
   "atk",
   "def",
   "crit",
   "er",
   "em",
   "dmg_bonus"
}

def build_showcase_data(uid, fields=None):
    """Fetch a UID's showcase and return a list of per-character dicts."""
    if fields is None:
        fields = DEFAULT_FIELDS

    showcase = fetch_showcase(uid)
    chars = fetch_character_metadata()
    loc = fetch_localization()
    artifacts = fetch_artifact_metadata()

    character_data_list = []
    for char in showcase["avatarInfoList"]:
        character_data = format_character(char, chars, loc, artifacts, fields)
        character_data_list.append(character_data)

    return character_data_list


def build_showcase_text(uid, fields=None):
    """Fetch a UID's showcase and return it as one line of text per character."""
    character_data = build_showcase_data(uid, fields)
    lines = []
    for data in character_data:
        line = format_character_line(data)
        lines.append(line)

    return "\n".join(lines)