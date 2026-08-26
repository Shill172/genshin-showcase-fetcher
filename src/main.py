import json
import os
import requests

def fetch_showcase(uid):
    """Fetch a player's live showcase data from Enka by UID."""
    url = f"https://enka.network/api/uid/{uid}"
    headers = {"User-Agent": "genshin-showcase-fetcher"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Showcase request failed: {response.status_code}")
    return response.json()


def fetch_character_metadata(path="resources/charbyid.json"):
    """Load character metadata from disk if cached, otherwise fetch and save it."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/avatars.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Character metadata request failed: {response.status_code}")

    data = response.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data

def fetch_artifact_metadata(path="resources/relics.json"):
    """Load artifact/artifact set metadata from disk if cached, otherwise fetch and save it."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/relics.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"artifact metadata request failed: {response.status_code}")

    data = response.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data

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


def fetch_localization(path="resources/loc.json"):
    """Load localization data from disk if cached, otherwise fetch and save it."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/locs.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Localization request failed: {response.status_code}")

    data = response.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data


def get_localized_name(name_hash, loc, lang="en"):
    """Resolve a TextMap hash to a readable localized name."""
    return loc[lang][str(name_hash)]


def get_character_name(avatar_id, chars, loc, lang="en"):
    """Resolve an avatarId to a readable character name."""
    name_hash = chars[str(avatar_id)]["NameTextMapHash"]
    return get_localized_name(name_hash, loc, lang)



def main():

    uid = 618285856

    showcase = fetch_showcase(uid)
    chars = fetch_character_metadata()
    loc = fetch_localization()
    artifacts = fetch_artifact_metadata()

    with open("output.txt", "w", encoding="utf-8") as f:

        for char in showcase["avatarInfoList"]:

            avatar_id = char["avatarId"]
            name = get_character_name(avatar_id, chars, loc)

            level = char.get("propMap", {}).get("4001", {}).get("val")

            talent_ids = char.get("talentIdList", [])
            constellation = len(talent_ids)

            refinement = None
            weapon_name = "No Weapon"

            for equip in char.get("equipList", []):

                if "weapon" in equip:
                    weapon = equip["weapon"]

                    weapon_name_hash = equip["flat"]["nameTextMapHash"]
                    weapon_name = get_localized_name(weapon_name_hash, loc)

                    affix_map = weapon.get("affixMap", {})

                    if affix_map:
                        refinement = next(iter(affix_map.values()))

                    break

            if refinement is not None:
                weapon_output = f"R{refinement + 1} {weapon_name}"
            else:
                weapon_output = weapon_name

            artifact_summary = get_artifact_summary(char, artifacts, loc)

            output = f"{name} Lv.{level}, C{constellation}, {weapon_output}, {artifact_summary}"

            print(output)
            f.write(output + "\n")


if __name__ == "__main__":
    main()