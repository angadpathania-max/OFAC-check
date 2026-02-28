const path = require("path");
const fs = require("fs");

const DATA_FILE = path.join(__dirname, "ofac_data.json");

const headers = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
};

exports.handler = async () => {
  try {
    const raw = fs.readFileSync(DATA_FILE, "utf8");
    const data = JSON.parse(raw);
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ entries: data.length }),
    };
  } catch (e) {
    if (e.code === "ENOENT") {
      return { statusCode: 200, headers, body: JSON.stringify({ entries: 0 }) };
    }
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: String(e.message || e), entries: 0 }),
    };
  }
};
