import requests 
import json

UID = 618285856
headers = {
        "User-Agent": "genshin-showcase-fetcher"
}

response = requests.get(
    f"https://enka.network/api/uid/{UID}",
    headers=headers
)

if response.status_code == 200:
    with open("resources/raw_response.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)
else:
    print(f"Request failed: {response.status_code}")