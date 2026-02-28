# OFAC Business Screening

A simple web app to screen business names against OFAC sanctions lists using fuzzy matching. Use it to check potential partners against the lists stored in the `OFAC DB` folder.

## Setup

1. **Python 3.10+** required.

2. **Install dependencies:**

   ```bash
   cd "D:\Personal\Courses\Cursor\OFAC check"
   pip install -r requirements.txt
   ```

3. **OFAC data:** Place OFAC Advanced XML files in the `OFAC DB` folder (e.g. `sdn_advanced.xml`, `cons_advanced.xml`). The app will load all `.xml` files from this folder into a local SQLite database.

## Run

```bash
cd "D:\Personal\Courses\Cursor\OFAC check"
python app.py
```

- On first run, the app creates `ofac_screening.db` and loads all XML files from `OFAC DB`. This can take a minute for large files.
- Open **http://127.0.0.1:5000** in your browser.

## Usage

1. Enter a **business name** in the search box.
2. Click **Search**. The backend runs a fuzzy match against all names in the OFAC lists.
3. **Possible matches** are shown with a match score (0–100), listed name, type (Name, A.K.A., etc.), source file, and reference.
4. Adjust **Min. match score** to include more (lower) or fewer (higher) results, and **Max results** to cap how many are returned.

## Reloading the database

After adding or updating XML files in `OFAC DB`, reload the database:

- **Option A:** Delete `ofac_screening.db` and restart the app (it will reload on startup if the DB is missing or empty).
- **Option B:** Call the load API (e.g. with curl or Postman):  
  `POST http://127.0.0.1:5000/api/load`

## Project layout

- `app.py` – Flask app, routes, and startup DB check
- `config.py` – Paths, DB path, fuzzy threshold, max results
- `database.py` – SQLite init and loading from XML
- `ofac_parser.py` – Parse OFAC Advanced XML and extract names
- `search_engine.py` – In-memory fuzzy search (RapidFuzz)
- `templates/index.html` – Frontend search form and results table
- `static/style.css` – Styles
- `OFAC DB/` – Folder containing OFAC XML files
- `ofac_screening.db` – SQLite DB (created at first run)

## Deploy to Netlify

You can host the screening tool on Netlify so anyone can use it in a browser.

1. **Push this project to a Git repo** (GitHub, GitLab, or Bitbucket).

2. **In Netlify:** [app.netlify.com](https://app.netlify.com) → **Add new site** → **Import an existing project**. Connect your Git provider and select this repository.

3. **Build settings** (Netlify should read these from `netlify.toml`):
   - **Build command:** `python scripts/export_ofac_data.py`
   - **Publish directory:** `public`
   - **Functions directory:** `netlify/functions`

4. **Deploy.** Netlify will run the build (which parses your `OFAC DB` XMLs and generates the data for the search function), then publish the site. Your site URL will be like `https://your-site-name.netlify.app`.

5. **Update OFAC data later:** Replace or add XML files in `OFAC DB`, push to Git; Netlify will rebuild and regenerate the list.

See **NETLIFY_DEPLOY.md** for more detailed steps.

## Disclaimer

This tool is for screening only. Always verify any potential match against official OFAC sources before making compliance or business decisions.
