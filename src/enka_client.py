"""Handles all network requests to Enka's UID endpoint and cached reference data."""

import requests
import json
import os

USER_AGENT = "genshin-showcase-fetcher"

def fetch_showcase(uid):
    """Fetch a player's live showcase data from Enka by UID."""
    url = f"https://enka.network/api/uid/{uid}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Showcase request failed: {response.status_code}")
    return response.json()


def fetch_character_metadata(path="resources/charbyid.json"):
    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/avatars.json"
    return fetch_cached_json(url, path)

def fetch_artifact_metadata(path="resources/relics.json"):
    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/relics.json"
    return fetch_cached_json(url, path)

def fetch_localization(path="resources/loc.json"):
    url = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/locs.json"
    return fetch_cached_json(url, path)


def load_etag(etag_path):
    if os.path.exists(etag_path):
        with open(etag_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_etag(etag_path, etag):
    with open(etag_path, "w", encoding="utf-8") as f:
        f.write(etag)


def fetch_cached_json(url, path):
    etag_path = path + ".etag"

    cached_etag = load_etag(etag_path)
    headers = {"User-Agent": USER_AGENT}

    if cached_etag and os.path.exists(path):
        headers["If-None-Match"] = cached_etag

    response = requests.get(url, headers=headers)

    if response.status_code == 304: # Nothing changed
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} for {url}")

    data = response.json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    new_etag = response.headers.get("ETag")
    if new_etag:
        save_etag(etag_path, new_etag)

    return data

