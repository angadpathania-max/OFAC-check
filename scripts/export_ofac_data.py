"""
Export OFAC list from XML files to JSON for Netlify Function.
Run from project root: python scripts/export_ofac_data.py
"""
import os
import sys
import json
import traceback

# Project root (parent of scripts/)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)


def main():
    print("Working directory:", os.getcwd())
    print("Project root (BASE):", BASE)

    ofac_folder = os.path.join(BASE, "OFAC DB")
    if not os.path.isdir(ofac_folder):
        print("ERROR: OFAC DB folder not found at:", ofac_folder, file=sys.stderr)
        sys.exit(1)

    xml_files = [f for f in os.listdir(ofac_folder) if f.endswith(".xml")]
    print("XML files in OFAC DB:", xml_files)
    if not xml_files:
        print("ERROR: No .xml files in OFAC DB folder.", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.join(BASE, "netlify", "functions", "ofac_data.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    from ofac_parser import load_all_xml_from_folder

    print("Loading XML from", ofac_folder, "...")
    records = load_all_xml_from_folder(ofac_folder)
    if not records:
        print("ERROR: No records parsed. Check that XML files are real content (not Git LFS pointers). Enable GIT_LFS_ENABLED=true in Netlify.", file=sys.stderr)
        sys.exit(1)

    data = [
        {
            "name": r["name"],
            "fixed_ref": r.get("fixed_ref", ""),
            "profile_id": r.get("profile_id", ""),
            "alias_type_id": r.get("alias_type_id", ""),
            "source_file": r.get("source_file", ""),
            "country": r.get("country", ""),
            "address": r.get("address", ""),
            "party_type": r.get("party_type", ""),
            "sanctions_program": r.get("sanctions_program", ""),
        }
        for r in records
    ]
    print("Writing", len(data), "entries to", out_path, "...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", str(e), file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
