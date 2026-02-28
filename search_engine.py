"""Fuzzy search against OFAC list."""
from rapidfuzz import fuzz, process
from config import FUZZY_THRESHOLD, MAX_MATCHES
from database import get_all_names


# Cache full list in memory for fast repeated searches
_cached_entries = None


def _get_entries():
    global _cached_entries
    if _cached_entries is None:
        rows = get_all_names()
        _cached_entries = [(row[1], row) for row in rows]  # (name, full_row)
    return _cached_entries


def fuzzy_search(query: str, threshold: int | None = None, max_results: int | None = None):
    """
    Fuzzy search query against OFAC names.
    Returns list of dicts: name, fixed_ref, profile_id, alias_type_id, source_file, score.
    """
    query = (query or "").strip()
    if not query:
        return []

    threshold = threshold if threshold is not None else FUZZY_THRESHOLD
    max_results = max_results if max_results is not None else MAX_MATCHES

    entries = _get_entries()
    names = [e[0] for e in entries]

    # Use token_set_ratio for better matching of word order / extra words
    results = process.extract(
        query,
        names,
        scorer=fuzz.token_set_ratio,
        limit=max_results,
        score_cutoff=threshold,
    )

    out = []
    for name, score, _ in results:
        # Find the row for this name (first match)
        row = next((e[1] for e in entries if e[0] == name), None)
        if row is None:
            continue
        out.append(
            {
                "name": row[1],
                "fixed_ref": row[2] or "",
                "profile_id": row[3] or "",
                "alias_type_id": row[4] or "",
                "source_file": row[5] or "",
                "score": int(score),
            }
        )
    return out


def invalidate_cache():
    """Clear cached OFAC list (call after reloading DB)."""
    global _cached_entries
    _cached_entries = None
