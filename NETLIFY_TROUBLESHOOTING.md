# Netlify "Network error" – troubleshooting

If the search form shows **"Network error. Please try again."**, the browser couldn’t get a valid response from the serverless function. After the next deploy, the site will show the **real error message** (e.g. "Screening list not available" or "Search failed (504)") so you can fix it.

---

## 1. Check the function in the browser

Open this URL in a new tab (replace `YOUR-SITE-NAME` with your Netlify site name):

**https://YOUR-SITE-NAME.netlify.app/.netlify/functions/search?name=test**

- If you see **JSON** with `"query"`, `"matches"`, `"count"` → the function works; the problem may be CORS or how the form calls it.
- If you see **404** → the function isn’t deployed or the path is wrong.
- If you see **503** and a message like "Screening list not available" → the function runs but `ofac_data.json` is missing (see step 3).
- If the page **never loads** or times out → function timeout or cold start (see step 4).

---

## 2. Check Netlify function logs

1. In Netlify: **Site → Functions** (or **Deploys → [latest deploy] → Functions**).
2. Open the **search** function and check **Logs** or **Invocations**.
3. Look for errors (e.g. `FileNotFoundError: ofac_data.json`, import errors, or timeouts).

---

## 3. Make sure `ofac_data.json` is built and included

The build runs `python scripts/export_ofac_data.py`, which should create **netlify/functions/ofac_data.json**.

- In **Deploys → [latest deploy] → Build log**, confirm you see something like:  
  `Writing 80008 entries to ... netlify/functions/ofac_data.json` and `Done.`
- If the script fails (e.g. "OFAC DB folder not found"), fix the repo so **OFAC DB** and the XML files are present (and, if you use Git LFS, that Netlify fetches LFS files).

**Netlify and Git LFS:**  
If your XMLs are in Git LFS, enable LFS in Netlify so the build gets real files, not pointers:

- **Site settings → Build & deploy → Environment** → add:
  - **Key:** `GIT_LFS_ENABLED`  
  - **Value:** `true`

Then trigger a new deploy.

---

## 4. Function timeout / cold start

Loading a large JSON on the first request can be slow. In **netlify.toml** the search function timeout is set to 26 seconds. If you still see timeouts:

- In Netlify: **Site settings → Functions** and check the configured timeout.
- Consider reducing the size of the data (e.g. fewer entries or a smaller JSON) if the function often times out.

---

## 5. Deploy the fixes and test again

After changing code or config:

1. Commit and push to your main branch.
2. Wait for the Netlify deploy to finish.
3. Reload the site and try a search again. You should now see a specific error message instead of "Network error" if something is still wrong.

---

## Quick checklist

| Check | Where |
|-------|--------|
| Build log shows "Writing ... entries to ... ofac_data.json" | Netlify → Deploys → Build log |
| Function URL returns JSON or a clear error | Browser: `/.netlify/functions/search?name=test` |
| Function logs show errors | Netlify → Functions → search → Logs |
| Git LFS enabled (if you use LFS) | Netlify → Site settings → Environment → `GIT_LFS_ENABLED=true` |
