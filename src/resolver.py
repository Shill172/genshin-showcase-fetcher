"""Resolves IDs and text hashes from Enka data into human-readable values."""

# Element stat map lookup for fightPropMap
ELEMENT_DMG_MAP = {
    40: "Pyro DMG",
    41: "Electro DMG",
    42: "Hydro DMG",
    43: "Dendro DMG",
    44: "Anemo DMG",
    45: "Geo DMG",
    46: "Cryo DMG",
    30: "Physical DMG",
}


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

def get_weapon_output(char, loc, lang="en"):
    """Resolve equipped weapon name + refinement into a display string."""
    for equip in char.get("equipList", []):
        if "weapon" in equip:
            weapon = equip["weapon"]
            weapon_name_hash = equip["flat"]["nameTextMapHash"]
            weapon_name = get_localized_name(weapon_name_hash, loc, lang)

            affix_map = weapon.get("affixMap", {})
            refinement = next(iter(affix_map.values())) if affix_map else None

            # Enka raw refinement is 0-indexed (0 = R1, 1 = R2, etc.)
            if refinement is not None:
                return f"R{refinement + 1} {weapon_name}"
            return weapon_name

    return "No Weapon"


def get_talents_summary(char, chars):
    """Resolve skill levels using SkillOrder and ProudMap from metadata."""
    avatar_id = str(char["avatarId"])
    char_info = chars.get(avatar_id, {})

    skill_order = char_info.get("SkillOrder", [])

    # ProudMap links a skill ID to its constellation upgrade ID
    proud_map = char_info.get("ProudMap", {})

    skills_map = char.get("skillLevelMap", {})
    extra_map = char.get("proudSkillExtraLevelMap", {})

    if not skills_map:
        return "Talents N/A"

    levels = []

    if skill_order:
        target_skills = skill_order
    else:
        target_skills = []
        for n in skills_map.keys():
            target_skills.append(int(n))

    for skill_id in target_skills:
        skill_key = str(skill_id)
        base_lvl = skills_map.get(skill_key, 1)

        proud_id = str(proud_map.get(skill_key, ""))

        # Check if Constellations (C3/C5) granted extra talent levels
        extra_lvl = extra_map.get(proud_id, 0)

        final_lvl = base_lvl + extra_lvl
        levels.append(str(final_lvl))

    return f"Talents {'/'.join(levels)}"


def get_highest_elemental_dmg(fight_map):
    """Find the highest elemental or physical damage bonus."""
    highest_val = 0.0
    highest_name = ""

    for prop_id, stat_name in ELEMENT_DMG_MAP.items():
        val = fight_map.get(str(prop_id), fight_map.get(prop_id, 0))
        if val > highest_val:
            highest_val = val
            highest_name = stat_name

    if highest_val > 0:
        return f"{highest_name} {highest_val * 100:.1f}%"
    return None

def format_character(char, chars, loc, artifacts, fields, lang="en"):
    """Build one line of showcase text based on requested fields."""
    avatar_id = char["avatarId"]
    parts = [get_character_name(avatar_id, chars, loc, lang)]
    
    fight_map = char.get("fightPropMap", {})

    if "level" in fields:
        # Enka propMap key "4001" stores character level
        level = char.get("propMap", {}).get("4001", {}).get("val")
        parts.append(f"Lv.{level}")

    if "constellation" in fields:
        constellation = len(char.get("talentIdList", []))
        parts.append(f"C{constellation}")

    if "weapon" in fields:
        parts.append(get_weapon_output(char, loc, lang))

    if "artifact_set" in fields:
        parts.append(get_artifact_summary(char, artifacts, loc, lang))

    if "friendship" in fields:
        friendship = char.get("fetterInfo", {}).get("expLevel", 1)
        parts.append(f"FLv.{friendship}")

    if "talents" in fields:
        parts.append(get_talents_summary(char, chars))

    # Key 2000 = Max HP, 2001 = ATK, 2002 = DEF
    if "hp" in fields:
        hp = round(fight_map.get(2000, 0))
        parts.append(f"HP {hp}")

    if "atk" in fields:
        atk = round(fight_map.get(2001, 0))
        parts.append(f"ATK {atk}")

    if "def" in fields:
        defense = round(fight_map.get(2002, 0))
        parts.append(f"DEF {defense}")

    if "crit" in fields:
        crit_rate = fight_map.get(20, 0) * 100
        crit_dmg = fight_map.get(22, 0) * 100
        parts.append(f"CRIT {crit_rate:.1f}%/{crit_dmg:.1f}%")

    if "er" in fields:
        er = fight_map.get(23, 0) * 100
        parts.append(f"ER {er:.1f}%")

    if "em" in fields:
        em = round(fight_map.get(28, 0))
        parts.append(f"EM {em}")

    if "dmg_bonus" in fields:
        elemental_bonus = get_highest_elemental_dmg(fight_map)
        if elemental_bonus:
            parts.append(elemental_bonus)

    return ", ".join(parts)


def get_localized_name(name_hash, loc, lang="en"):
    """Resolve a TextMap hash to a readable localized name."""
    return loc[lang][str(name_hash)]


def get_character_name(avatar_id, chars, loc, lang="en"):
    """Resolve an avatarId to a readable character name."""
    name_hash = chars[str(avatar_id)]["NameTextMapHash"]
    return get_localized_name(name_hash, loc, lang)