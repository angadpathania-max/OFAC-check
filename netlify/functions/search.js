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

function search(query, threshold, maxResults) {
  threshold = threshold != null ? threshold : DEFAULT_THRESHOLD;
  maxResults = maxResults != null ? maxResults : DEFAULT_MAX;
  query = (query || "").trim();
  if (!query) return [];

  const entries = loadData();
  const names = entries.map((e) => e.name);

  const results = fuzzball.extract(query, names, {
    scorer: fuzzball.token_set_ratio,
    limit: maxResults,
    cutoff: threshold,
  });

  return results.map(([name, score]) => {
    const row = entries.find((e) => e.name === name) || {};
    return {
      name: row.name || name,
      fixed_ref: row.fixed_ref || "",
      profile_id: row.profile_id || "",
      alias_type_id: row.alias_type_id || "",
      source_file: row.source_file || "",
      score: Math.round(score),
    };
  });
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
