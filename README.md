# Genshin Showcase Fetcher

A command-line tool that fetches a player's character showcase from [Enka Network](https://enka.network/) and prints a readable summary of each character's level, constellation, weapon, and equipped artifact set.

## Example Output
```
Amber Lv.90, C6, R2 Skyward Harp, 2pc Bloodstained Chivalry + 2pc Pale Flame
Bennett Lv.90, C6, R1 Freedom-Sworn, 4pc Noblesse Oblige
```

## Requirements

- Python 3.10+
- A public Genshin Impact UID with the in-game showcase enabled

## Installation

1. Clone the repo:
```bash
   git clone https://github.com/Shill172/genshin-showcase-fetcher.git
   cd genshin-showcase-fetcher
```
2. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

```bash
python src/main.py <uid>
```

Example:
```bash
python src/main.py 618285856
```

Run with `-h` for help:
```bash
python src/main.py -h
```

## How It Works

- Fetches live showcase data from Enka's API for the given UID
- Fetches character/localization/artifact reference data from Enka's [API-docs repo](https://github.com/EnkaNetwork/API-docs), caching it locally and using HTTP ETags to avoid re-downloading unchanged data
- Resolves numeric IDs and text hashes into readable names
- Prints a formatted summary and saves it to `output.txt`

## Credits

Built using data from [Enka Network](https://enka.network/). This project is not affiliated with HoYoverse or Enka Network.
