const path = require("path");
const fs = require("fs");
const fuzzball = require("fuzzball");

const DATA_FILE = path.join(__dirname, "ofac_data.json");
const DEFAULT_THRESHOLD = 60;
const DEFAULT_MAX = 100;

let _entries = null;

function loadData() {
  if (_entries === null) {
    try {
      const raw = fs.readFileSync(DATA_FILE, "utf8");
      _entries = JSON.parse(raw);
    } catch (e) {
      if (e.code === "ENOENT") _entries = [];
      else throw e;
    }
  }
  return _entries;
}

function rowToMatch(row, score) {
  return {
    name: row.name || "",
    fixed_ref: row.fixed_ref || "",
    profile_id: row.profile_id || "",
    alias_type_id: row.alias_type_id || "",
    source_file: row.source_file || "",
    score: Math.round(score),
  };
}

function search(query, threshold, maxResults) {
  threshold = threshold != null ? threshold : DEFAULT_THRESHOLD;
  maxResults = maxResults != null ? maxResults : DEFAULT_MAX;
  query = (query || "").trim();
  if (!query) return [];

  const entries = loadData();
  const names = entries.map((e) => e.name);
  const qLower = query.toLowerCase();

  // 1) Contains match: any listed name that contains the query (case-insensitive) gets score 95
  const containsSet = new Set();
  const containsMatches = [];
  for (let i = 0; i < entries.length; i++) {
    if (entries[i].name && entries[i].name.toLowerCase().includes(qLower)) {
      containsSet.add(entries[i].name);
      containsMatches.push(rowToMatch(entries[i], 95));
    }
  }

  // 2) Fuzzy match: token_set_ratio = best for names (word order, extra words, typos).
  //    threshold (cutoff) = only include fuzzy results with score >= this (e.g. 60 = permissive, 90 = strict).
  const fuzzyResults = fuzzball.extract(query, names, {
    scorer: fuzzball.token_set_ratio,
    limit: maxResults,
    cutoff: threshold,
  });

  const seen = new Set(containsSet);
  const fuzzyMatches = [];
  for (const [name, score] of fuzzyResults) {
    if (seen.has(name)) continue;
    seen.add(name);
    const row = entries.find((e) => e.name === name) || {};
    fuzzyMatches.push(rowToMatch(row, score));
  }

  // 3) Merge: contains first (score 95), then fuzzy; sort by score desc, take top maxResults
  const merged = [...containsMatches, ...fuzzyMatches]
    .sort((a, b) => b.score - a.score)
    .slice(0, maxResults);

  return merged;
}

const headers = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type",
};

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers, body: "" };
  }

  const params = event.queryStringParameters || {};
  const name = (params.name || "").trim();

  if (!name) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: "Please provide a business name.", matches: [] }),
    };
  }

  let threshold = DEFAULT_THRESHOLD;
  let maxResults = DEFAULT_MAX;
  try {
    if (params.threshold != null) threshold = parseInt(params.threshold, 10);
  } catch (_) {}
  try {
    if (params.max != null) maxResults = parseInt(params.max, 10);
  } catch (_) {}

  try {
    const matches = search(name, threshold, maxResults);
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ query: name, matches, count: matches.length }),
    };
  } catch (e) {
    if (e.code === "ENOENT" || (e.message && e.message.includes("ofac_data"))) {
      return {
        statusCode: 503,
        headers,
        body: JSON.stringify({
          error: "Screening list not available. Re-run build.",
          matches: [],
        }),
      };
    }
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: String(e.message || e), matches: [] }),
    };
  }
};
