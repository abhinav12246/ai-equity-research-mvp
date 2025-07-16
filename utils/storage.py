import os
import json
import hashlib

CACHE_DIR = ".cache"
DB_FILE = "reports.json"

def _make_cache_key(ticker: str, text: str):
    key = f"{ticker}_{hashlib.md5(text.encode()).hexdigest()}"
    return os.path.join(CACHE_DIR, key + ".json")

def load_from_cache(ticker, text):
    path = _make_cache_key(ticker, text)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_to_cache(ticker, text, data):
    path = _make_cache_key(ticker, text)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def append_to_db(insight: dict):
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

    with open(DB_FILE, "r") as f:
        data = json.load(f)

    data.append(insight)

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
