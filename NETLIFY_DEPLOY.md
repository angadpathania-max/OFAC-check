# Deploy OFAC Screening to Netlify

This guide walks you through putting the OFAC Business Screening site on Netlify so users can enter a business name and see possible matches.

## What Netlify does

- **Build:** Runs `python scripts/export_ofac_data.py`, which reads all XML files from `OFAC DB` and writes `netlify/functions/ofac_data.json`.
- **Publish:** Serves the static site from the `public` folder (the search page and CSS).
- **Functions:** Runs serverless search and stats APIs that use the generated JSON.

No Flask server or database runs on Netlify; search is handled by serverless functions.

## Prerequisites

- The project in a **Git repository** (GitHub, GitLab, or Bitbucket).
- The **OFAC DB** folder in that repo with at least one OFAC Advanced XML file (e.g. `sdn_advanced.xml`, `cons_advanced.xml`).

## Step 1: Push to Git

If the project is not in a repo yet:

```bash
cd "D:\Personal\Courses\Cursor\OFAC check"
git init
git add .
git commit -m "OFAC screening site with Netlify support"
```

Create a new repository on GitHub/GitLab/Bitbucket, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 2: Connect to Netlify

1. Log in at [app.netlify.com](https://app.netlify.com).
2. Click **Add new site** → **Import an existing project**.
3. Choose your Git provider and authorize Netlify.
4. Select the repository that contains this project.
5. Netlify will read **netlify.toml** and fill in:
   - **Build command:** `python scripts/export_ofac_data.py`
   - **Publish directory:** `public`
   - **Functions directory:** `netlify/functions`
6. Click **Deploy site**.

## Step 3: Wait for the build

The first build may take 2–5 minutes because it:

- Parses all XML files in `OFAC DB`
- Writes `ofac_data.json` for the functions
- Installs Python dependencies for the functions (e.g. rapidfuzz)
- Publishes the site and functions

If the build fails, check the build log. Common issues:

- **"OFAC DB folder not found"** – Ensure `OFAC DB` and its XML files are committed and in the repo root.
- **Python errors** – Netlify uses Python 3.11 by default (set in netlify.toml). If you need another version, set `PYTHON_VERSION` in Netlify **Site settings → Environment variables**.

## Step 4: Use your site

When the deploy finishes, Netlify shows a URL like:

**https://random-name-12345.netlify.app**

Open it: you should see the OFAC Business Screening page. Enter a business name, click Search, and the possible matches will load from the serverless search function.

## Optional: Custom domain

In Netlify: **Site configuration → Domain management → Add custom domain**. You can use a subdomain (e.g. `ofac.yourcompany.com`) or connect a domain you own.

## Updating the OFAC list

1. Add or replace XML files in the `OFAC DB` folder locally.
2. Commit and push to your default branch (e.g. `main`).
3. Netlify will run a new build, regenerate `ofac_data.json`, and redeploy. The live site will use the new list after the deploy completes.

## Local test of Netlify build

To simulate the Netlify build on your machine:

```bash
cd "D:\Personal\Courses\Cursor\OFAC check"
python scripts/export_ofac_data.py
```

Then run the Netlify CLI (optional):

```bash
npm install -g netlify-cli
netlify dev
```

This serves the site and runs the functions locally so you can test before pushing.
