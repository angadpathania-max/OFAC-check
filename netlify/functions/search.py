"""
Netlify serverless function: fuzzy search over OFAC list.
Expects ofac_data.json in the same directory (generated at build time).
"""
import os
import json
from rapidfuzz import fuzz, process

DATA_FILE = os.path.join(os.path.dirname(__file__), "ofac_data.json")
DEFAULT_THRESHOLD = 60
DEFAULT_MAX = 100

_entries = None


def load_data():
    global _entries
    if _entries is None:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            _entries = json.load(f)
    return _entries


def search(query, threshold=None, max_results=None):
    threshold = threshold if threshold is not None else DEFAULT_THRESHOLD
    max_results = max_results if max_results is not None else DEFAULT_MAX
    query = (query or "").strip()
    if not query:
        return []

    entries = load_data()
    names = [e["name"] for e in entries]

    results = process.extract(
        query,
        names,
        scorer=fuzz.token_set_ratio,
        limit=max_results,
        score_cutoff=threshold,
    )

    out = []
    for name, score, _ in results:
        row = next((e for e in entries if e["name"] == name), None)
        if row:
            out.append(
                {
                    "name": row["name"],
                    "fixed_ref": row.get("fixed_ref", ""),
                    "profile_id": row.get("profile_id", ""),
                    "alias_type_id": row.get("alias_type_id", ""),
                    "source_file": row.get("source_file", ""),
                    "score": int(score),
                }
            )
    return out


def handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": headers, "body": ""}

    params = event.get("queryStringParameters") or {}
    name = (params.get("name") or "").strip()

    if not name:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
                {"error": "Please provide a business name.", "matches": []}
            ),
        }

    try:
        threshold = int(params.get("threshold", DEFAULT_THRESHOLD))
    except (TypeError, ValueError):
        threshold = DEFAULT_THRESHOLD

    try:
        max_results = int(params.get("max", DEFAULT_MAX))
    except (TypeError, ValueError):
        max_results = DEFAULT_MAX

    try:
        matches = search(name, threshold=threshold, max_results=max_results)
    except FileNotFoundError:
        return {
            "statusCode": 503,
            "headers": headers,
            "body": json.dumps(
                {"error": "Screening list not available. Re-run build.", "matches": []}
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e), "matches": []}),
        }

    body = json.dumps(
        {"query": name, "matches": matches, "count": len(matches)},
        ensure_ascii=False,
    )
    return {"statusCode": 200, "headers": headers, "body": body}
