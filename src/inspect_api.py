"""
Task 2.3 - Retrieve and inspect the instructor-provided REST API.

Fill in API_URL below with the URL posted on the LMS, then run this script.
It saves the raw JSON to data/raw/api_snapshot.json and prints the
retrieval timestamp you should paste into docs/source_inventory.md.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "<API_URL_FROM_LMS>"  # <-- replace with the real endpoint
TIMEOUT_SECONDS = 20
OUTPUT_PATH = Path("data/raw/api_snapshot.json")


def main() -> None:
    if API_URL == "<API_URL_FROM_LMS>":
        raise SystemExit("Set API_URL to the endpoint given in the LMS before running this script.")

    response = requests.get(API_URL, timeout=TIMEOUT_SECONDS)

    print("status:", response.status_code)
    response.raise_for_status()  # fail clearly if unsuccessful

    content_type = response.headers.get("Content-Type")
    print("content-type:", content_type)

    payload = response.json()
    top_level_type = type(payload).__name__
    print("top-level type:", top_level_type)

    if isinstance(payload, list):
        print("record count:", len(payload))
        sample = payload[0] if payload else None
    elif isinstance(payload, dict):
        # Try to find a likely list of records inside the dict
        list_fields = [k for k, v in payload.items() if isinstance(v, list)]
        print("dict keys:", list(payload.keys()))
        if list_fields:
            print(f"record count (field '{list_fields[0]}'):", len(payload[list_fields[0]]))
        sample = payload
    else:
        sample = payload

    print("sample record:", json.dumps(sample, indent=2, ensure_ascii=False)[:1000])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    print("retrieved_at_utc:", retrieved_at)
    print(f"Saved snapshot to {OUTPUT_PATH}")
    print("\n>> Copy this line into docs/source_inventory.md:")
    print(f">> Retrieved at (UTC): {retrieved_at}")


if __name__ == "__main__":
    main()
