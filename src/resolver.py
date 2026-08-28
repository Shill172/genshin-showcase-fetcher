"""Resolves IDs and text hashes from Enka data into human-readable values."""

def get_artifact_summary(char, artifacts, loc, lang="en"):
    """Count equipped artifact pieces per set, return a label like
    '4pc Noblesse Oblige', '2pc SetA + 2pc SetB', or 'No set'."""
    set_counts = {}

    for equip in char.get("equipList", []):
        if "reliquary" not in equip:
            continue  # skip the weapon
        set_id = str(equip["flat"]["setId"])
        set_counts[set_id] = set_counts.get(set_id, 0) + 1

    four_piece = []
    for sid, count in set_counts.items():
        if count >= 4:
            four_piece.append(sid)

    if four_piece:
        name_hash = artifacts["Sets"][four_piece[0]]["Name"]
        return f"4pc {get_localized_name(name_hash, loc, lang)}"


    two_piece = []
    for sid, count in set_counts.items():
        if count >= 2:
            two_piece.append(sid)

    if two_piece:
        names = []
        for sid in two_piece:
            set_name_hash = artifacts["Sets"][sid]["Name"]
            resolved_name = get_localized_name(set_name_hash, loc, lang)
            names.append(resolved_name)

        labels = []
        for n in names:
            labels.append(f"2pc {n}")

        return " + ".join(labels)

    return "No set"


def get_localized_name(name_hash, loc, lang="en"):
    """Resolve a TextMap hash to a readable localized name."""
    return loc[lang][str(name_hash)]


def get_character_name(avatar_id, chars, loc, lang="en"):
    """Resolve an avatarId to a readable character name."""
    name_hash = chars[str(avatar_id)]["NameTextMapHash"]
    return get_localized_name(name_hash, loc, lang)