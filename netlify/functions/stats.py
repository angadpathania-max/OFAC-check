"""Netlify function: return OFAC list entry count."""
import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), "ofac_data.json")


def handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"entries": len(data)}),
        }
    except FileNotFoundError:
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"entries": 0}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e), "entries": 0}),
        }
