"""Fetches a player's showcase and prints/saves a formatted summary."""

from enka_client import fetch_showcase, fetch_character_metadata, fetch_localization, fetch_artifact_metadata
from resolver import get_character_name, get_artifact_summary, get_localized_name

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