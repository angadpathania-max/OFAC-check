"""Flask app for OFAC business screening."""
import os
from flask import Flask, request, jsonify, render_template
from config import OFAC_DB_FOLDER, DATABASE_PATH
from database import init_db, load_ofac_data, get_connection
from search_engine import fuzzy_search, invalidate_cache

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["GET", "POST"])
def search():
    """Search OFAC list by business name (fuzzy)."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
    else:
        name = (request.args.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Please provide a business name.", "matches": []}), 400

    j = request.get_json(silent=True) or {}
    threshold = request.args.get("threshold", type=int) or j.get("threshold")
    max_results = request.args.get("max", type=int) or j.get("max")

    matches = fuzzy_search(name, threshold=threshold, max_results=max_results)
    return jsonify({"query": name, "matches": matches, "count": len(matches)})


@app.route("/api/load", methods=["POST"])
def load_db():
    """Reload OFAC data from XML files (admin/init)."""
    if not os.path.isdir(OFAC_DB_FOLDER):
        return jsonify({"error": f"OFAC DB folder not found: {OFAC_DB_FOLDER}"}), 500
    try:
        count = load_ofac_data(replace=True)
        invalidate_cache()
        return jsonify({"message": f"Loaded {count} entries from OFAC DB."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats")
def stats():
    """Return count of entries in DB."""
    try:
        conn = get_connection()
        cur = conn.execute("SELECT COUNT(*) FROM ofac_entries")
        n = cur.fetchone()[0]
        conn.close()
        return jsonify({"entries": n})
    except Exception as e:
        return jsonify({"error": str(e), "entries": 0}), 500


def ensure_db():
    """Create DB and load data if DB is missing or empty."""
    if not os.path.isfile(DATABASE_PATH):
        init_db()
        if os.path.isdir(OFAC_DB_FOLDER):
            load_ofac_data(replace=True)
    else:
        conn = get_connection()
        cur = conn.execute("SELECT COUNT(*) FROM ofac_entries")
        if cur.fetchone()[0] == 0 and os.path.isdir(OFAC_DB_FOLDER):
            conn.close()
            load_ofac_data(replace=True)
        else:
            conn.close()


if __name__ == "__main__":
    ensure_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
