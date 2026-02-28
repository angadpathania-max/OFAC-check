"""
Export OFAC list from XML files to JSON for Netlify Function.
Run from project root: python scripts/export_ofac_data.py
"""
import os
import sys
import json

# Project root (parent of scripts/)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from ofac_parser import load_all_xml_from_folder


def main():
    ofac_folder = os.path.join(BASE, "OFAC DB")
    if not os.path.isdir(ofac_folder):
        print(f"OFAC DB folder not found: {ofac_folder}", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.join(BASE, "netlify", "functions", "ofac_data.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print("Loading XML from", ofac_folder, "...")
    records = load_all_xml_from_folder(ofac_folder)
    # Keep only fields needed for search response
    data = [
        {
            "name": r["name"],
            "fixed_ref": r.get("fixed_ref", ""),
            "profile_id": r.get("profile_id", ""),
            "alias_type_id": r.get("alias_type_id", ""),
            "source_file": r.get("source_file", ""),
        }
        for r in records
    ]
    print(f"Writing {len(data)} entries to {out_path} ...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Done.")


if __name__ == "__main__":
    main()
