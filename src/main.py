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


def get_character_name(avatar_id, chars, loc, lang="en"):
    """Resolve an avatarId to a readable character name."""
    name_hash = chars[str(avatar_id)]["NameTextMapHash"]
    return loc[lang][str(name_hash)]


def main():
    uid = 618285856

    showcase = fetch_showcase(uid)
    chars = fetch_character_metadata()
    loc = fetch_localization()

    for char in showcase["avatarInfoList"]:
        avatar_id = char["avatarId"]
        name = get_character_name(avatar_id, chars, loc)
        print(name)


if __name__ == "__main__":
    main()