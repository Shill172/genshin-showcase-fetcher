"""Fetches a player's showcase and prints/saves a formatted summary."""
import argparse
from showcase import build_showcase_text


def main():
    parser = argparse.ArgumentParser(description="Fetch and display a Genshin Impact showcase from Enka Network.")
    parser.add_argument("uid", type=int, help="The player's UID to look up")
    args = parser.parse_args()

    text = build_showcase_text(args.uid)

    print(text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()